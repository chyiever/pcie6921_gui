"""PCIe-6921 API 边界层的无硬件测试。"""

import sys
import unittest
from pathlib import Path

import numpy as np


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from pcie6921_api import AlignedBuffer


class AlignedBufferTests(unittest.TestCase):
    """验证 DMA 缓冲区地址与 ctypes 指针类型。"""

    def test_int16_buffer_is_4k_aligned(self):
        buffer = AlignedBuffer(1024, np.int16)
        self.assertEqual(buffer._aligned_addr % 4096, 0)
        self.assertEqual(buffer.array.dtype, np.int16)

    def test_phase_and_monitor_types(self):
        self.assertEqual(AlignedBuffer(8, np.int32).array.dtype, np.int32)
        self.assertEqual(AlignedBuffer(8, np.uint32).array.dtype, np.uint32)


if __name__ == "__main__":
    unittest.main()
