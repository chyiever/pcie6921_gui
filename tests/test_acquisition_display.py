"""Acquisition display snapshot behavior tests."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from acquisition_thread import AcquisitionThread
from config import AllParams, DataSource


class AcquisitionDisplaySnapshotTests(unittest.TestCase):
    """Verify display-only frame sizing follows PHASE crop settings."""

    def test_single_channel_phase_display_points_use_crop_width(self):
        params = AllParams()
        params.upload.data_source = DataSource.PHASE
        params.upload.channel_num = 1
        params.basic.point_num_per_scan = 1000
        params.phase_demod.merge_point_num = 10
        params.phase_demod.crop_distance_start = 20
        params.phase_demod.crop_distance_end = 70

        thread = AcquisitionThread(None)
        thread.configure(params)

        self.assertEqual(thread._point_num_after_merge, 100)
        self.assertEqual(thread._display_points_per_frame(DataSource.PHASE, 1), 50)

    def test_dual_channel_phase_display_points_keep_uncropped_width(self):
        params = AllParams()
        params.upload.data_source = DataSource.PHASE
        params.upload.channel_num = 2
        params.basic.point_num_per_scan = 1000
        params.phase_demod.merge_point_num = 10
        params.phase_demod.crop_distance_start = 20
        params.phase_demod.crop_distance_end = 70

        thread = AcquisitionThread(None)
        thread.configure(params)

        self.assertEqual(thread._display_points_per_frame(DataSource.PHASE, 2), 100)


if __name__ == "__main__":
    unittest.main()
