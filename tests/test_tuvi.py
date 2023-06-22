import unittest

from core.tuvi.elements.gioitinh import GioiTinh
from core.tuvi.utils import TuViUtil
from core.date import Date


class TestTuVi(unittest.TestCase):
    def test_tuvi_amduong(self):
        self.assertEqual(TuViUtil.tim_am_duong(Date(2002, 3, 1), GioiTinh.NAM.value), 'Dương Nam')
        self.assertEqual(TuViUtil.tim_am_duong(Date(1997, 7, 28, 5, 0), GioiTinh.NU.value), 'Âm Nữ')
        self.assertEqual(TuViUtil.tim_am_duong(Date(1994, 11, 2, 16, 0), GioiTinh.NU.value), 'Dương Nữ')
        self.assertEqual(TuViUtil.tim_am_duong(Date(1997, 12, 25, 20, 0), GioiTinh.NU.value), 'Âm Nữ')
        self.assertEqual(TuViUtil.tim_am_duong(Date(2002, 8, 16, 10, 30), GioiTinh.NU.value), 'Dương Nữ')
    

    def test_tuvi_cuc(self):
        self.assertEqual(TuViUtil.tim_cuc(Date(1991, 7, 3, 5, 50)), 'Mộc tam cục')
        self.assertEqual(TuViUtil.tim_cuc(Date(1997, 7, 28, 5, 0)), 'Hoả lục cục')
        self.assertEqual(TuViUtil.tim_cuc(Date(1994, 11, 2, 16, 0)), 'Hoả lục cục')
        self.assertEqual(TuViUtil.tim_cuc(Date(1997, 12, 25, 20, 0)), 'Kim tứ cục')
        self.assertEqual(TuViUtil.tim_cuc(Date(2002, 8, 16, 10, 30)), 'Kim tứ cục')


    def test_tuvi_menh(self):
        self.assertEqual(TuViUtil.tim_menh(Date(1991, 7, 3, 5, 50)), 'Lộ Bàng Thổ')
        self.assertEqual(TuViUtil.tim_menh(Date(1997, 7, 28, 5, 0)), 'Giản Hạ Thuỷ')
        self.assertEqual(TuViUtil.tim_menh(Date(1994, 11, 2, 16, 0)), 'Sơn Đầu Hoả')
        self.assertEqual(TuViUtil.tim_menh(Date(1997, 12, 25, 20, 0)), 'Giản Hạ Thuỷ')
        self.assertEqual(TuViUtil.tim_menh(Date(2002, 8, 16, 10, 30)), 'Dương Liễu Mộc')


    def test_tuvi_chu_menh(self):
        self.assertEqual(TuViUtil.tim_chu_menh(Date(1991, 7, 3, 5, 50)), 'Văn Khúc')
        self.assertEqual(TuViUtil.tim_chu_menh(Date(1997, 7, 28, 5, 0)), 'Liêm Trinh')
        self.assertEqual(TuViUtil.tim_chu_menh(Date(1994, 11, 2, 16, 0)), 'Lộc Tồn')
        self.assertEqual(TuViUtil.tim_chu_menh(Date(1997, 12, 25, 20, 0)), 'Lộc Tồn')
        self.assertEqual(TuViUtil.tim_chu_menh(Date(2002, 8, 16, 10, 30)), 'Văn Khúc')


    def test_tuvi_chu_than(self):
        self.assertEqual(TuViUtil.tim_chu_than(Date(1991, 7, 3, 5, 50)), 'Thiên Tướng')
        self.assertEqual(TuViUtil.tim_chu_than(Date(1997, 7, 28, 5, 0)), 'Thiên Tướng')
        self.assertEqual(TuViUtil.tim_chu_than(Date(1994, 11, 2, 16, 0)), 'Văn Xương')
        self.assertEqual(TuViUtil.tim_chu_than(Date(1997, 12, 25, 20, 0)), 'Thiên Tướng')
        self.assertEqual(TuViUtil.tim_chu_than(Date(2002, 8, 16, 10, 30)), 'Hoả Tinh')


    def test_tuvi_tinh_ly_am_duong(self):
        self.assertEqual(TuViUtil.tim_tinh_ly_am_duong(Date(1991, 7, 3, 5, 50)), 'Âm Dương thuận lý')
        self.assertEqual(TuViUtil.tim_tinh_ly_am_duong(Date(1997, 7, 28, 5, 0)), 'Âm Dương nghịch lý')
        self.assertEqual(TuViUtil.tim_tinh_ly_am_duong(Date(1994, 11, 2, 16, 0)), 'Âm Dương thuận lý')
        self.assertEqual(TuViUtil.tim_tinh_ly_am_duong(Date(1997, 12, 25, 20, 0)), 'Âm Dương nghịch lý')
        self.assertEqual(TuViUtil.tim_tinh_ly_am_duong(Date(2002, 8, 16, 10, 30)), 'Âm Dương nghịch lý')


    def test_tuvi_menh_cuc_sinh_khac(self):
        self.assertEqual(TuViUtil.tim_cuc_menh_sinh_khac(Date(1991, 7, 3, 5, 50)), 'Cục khắc Mệnh')
        self.assertEqual(TuViUtil.tim_cuc_menh_sinh_khac(Date(1997, 7, 28, 5, 0)), 'Mệnh khắc Cục')
        self.assertEqual(TuViUtil.tim_cuc_menh_sinh_khac(Date(1994, 11, 2, 16, 0)), 'Mệnh Cục bình hoà')
        self.assertEqual(TuViUtil.tim_cuc_menh_sinh_khac(Date(1997, 12, 25, 20, 0)), 'Cục sinh Mệnh')
        self.assertEqual(TuViUtil.tim_cuc_menh_sinh_khac(Date(2002, 8, 16, 10, 30)), 'Cục khắc Mệnh')


    def test_tuvi_noi_cu_than(self):
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(1991, 7, 3, 5, 50), GioiTinh.NAM.value), 'Thân cư Thiên Di')
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(1997, 7, 28, 5, 0), GioiTinh.NU.value), 'Thân cư Thiên Di')
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(1994, 11, 2, 16, 0), GioiTinh.NU.value), 'Thân cư Quan Lộc')
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(1997, 12, 25, 20, 0), GioiTinh.NU.value), 'Thân cư Tài Bạch')
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(2002, 8, 16, 10, 30), GioiTinh.NU.value), 'Thân cư Phu')
        self.assertEqual(TuViUtil.tim_noi_cu_than(Date(2002, 8, 16, 11, 30), GioiTinh.NU.value), 'Thân Mệnh đồng cung')



if __name__ == '__main__':
    unittest.main()
