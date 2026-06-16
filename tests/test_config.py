"""PCIe-6921 参数模型与设备约束测试。"""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from config import ClockSource, DataSource, calculate_fiber_length, validate_point_num


class ConfigValidationTests(unittest.TestCase):
    """验证 6921 与 7821 不兼容的关键参数规则。"""

    def test_clock_source_encoding_is_6921_specific(self):
        self.assertEqual(int(ClockSource.EXTERNAL), 0)
        self.assertEqual(int(ClockSource.INTERNAL), 1)

    def test_raw_uses_256_point_alignment(self):
        self.assertEqual(validate_point_num(20480, 2, DataSource.raw), (True, ""))
        self.assertFalse(validate_point_num(20481, 2, DataSource.raw)[0])

    def test_dual_demodulation_uses_128_point_alignment(self):
        self.assertEqual(validate_point_num(65536, 2, DataSource.I_Q), (True, ""))
        self.assertFalse(validate_point_num(65664, 2, DataSource.I_Q)[0])

    def test_phase_has_no_alignment_requirement(self):
        self.assertEqual(validate_point_num(65535, 1, DataSource.PHASE), (True, ""))
        self.assertFalse(validate_point_num(65537, 1, DataSource.PHASE)[0])

    def test_upload_rate_controls_spatial_distance(self):
        self.assertEqual(calculate_fiber_length(1000, 1, DataSource.PHASE, 1), 400.0)
        self.assertEqual(calculate_fiber_length(1000, 5, DataSource.PHASE, 5), 2000.0)


if __name__ == "__main__":
    unittest.main()
