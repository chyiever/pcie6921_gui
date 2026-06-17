"""Data saver statistics and rotation tests."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from data_saver import FrameBasedFileSaver


class FrameBasedFileSaverTests(unittest.TestCase):
    """Verify frame-based saving reports totals across rotated files."""

    def test_total_bytes_include_rotated_files_and_stop_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            saver = FrameBasedFileSaver(save_path=tmp, frames_per_file=2, buffer_size=8)
            frame = np.arange(16, dtype=np.int32)

            saver.start(scan_rate=4000, points_per_frame=16)
            self.assertTrue(saver.save_frame(frame))
            self.assertTrue(saver.save_frame(frame))
            self.assertTrue(saver.save_frame(frame))
            saver.stop()

            expected_bytes = frame.nbytes * 3
            self.assertEqual(saver.blocks_written, 3)
            self.assertEqual(saver.total_bytes_all_files, expected_bytes)

            snapshot = saver.get_diagnostics_snapshot()
            self.assertEqual(snapshot["total_bytes"], expected_bytes)
            self.assertIn("write_p95_ms", snapshot)
            self.assertIn("write_slow_count", snapshot)

            # A second stop must not re-log or mutate final accounting.
            saver.stop()
            self.assertEqual(saver.total_bytes_all_files, expected_bytes)


if __name__ == "__main__":
    unittest.main()
