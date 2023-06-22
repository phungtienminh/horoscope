import unittest

from core.tuvi.elements.nguhanh import NguHanh
from core.utils import NguHanhUtil


class TestNguHanh(unittest.TestCase):
    def test_ngu_hanh_tuong_sinh(self):
        self.assertTrue(NguHanhUtil.check_tuong_sinh(NguHanh.THUY, NguHanh.MOC))
        self.assertFalse(NguHanhUtil.check_tuong_sinh(NguHanh.THUY, NguHanh.HOA))

    
    def test_ngu_hanh_tuong_khac(self):
        self.assertTrue(NguHanhUtil.check_tuong_khac(NguHanh.THUY, NguHanh.HOA))
        self.assertTrue(NguHanhUtil.check_tuong_khac(NguHanh.MOC, NguHanh.THO))


if __name__ == '__main__':
    unittest.main()
