import unittest

from core.date import Date
from core.utils import ZodiacUtil


class TestZodiac(unittest.TestCase):
    def test_zodiac_year(self):
        # 1st batch
        self.assertEqual(ZodiacUtil.zodiac_year(Date(2002, 1, 1)), 'Nhâm Ngọ')
        self.assertEqual(ZodiacUtil.zodiac_year(Date(1996, 1, 1)), 'Bính Tí')
        self.assertEqual(ZodiacUtil.zodiac_year(Date(2004, 1, 1)), 'Giáp Thân')
        self.assertEqual(ZodiacUtil.zodiac_year(Date(2005, 1, 1)), 'Ất Dậu')
        self.assertEqual(ZodiacUtil.zodiac_year(Date(1993, 1, 1)), 'Quý Dậu')

        # 2nd batch
        self.assertEqual(ZodiacUtil.zodiac_year(Date(1995, 11, 22)), 'Ất Hợi')
        self.assertEqual(ZodiacUtil.zodiac_year(Date(1997, 4, 27)), 'Đinh Sửu')


    def test_zodiac_month(self):
        self.assertEqual(ZodiacUtil.zodiac_month(Date(1995, 11, 22)), 'Mậu Tí')
        self.assertEqual(ZodiacUtil.zodiac_month(Date(1997, 4, 27)), 'Ất Tỵ')


    def test_zodiac_day(self):
        self.assertEqual(ZodiacUtil.zodiac_day(Date(1996, 1, 12)), 'Mậu Thân')
        self.assertEqual(ZodiacUtil.zodiac_day(Date(1997, 6, 2)), 'Ất Hợi')


    def test_zodiac_hour(self):
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(2004, 2, 20, 6, 55)), 'Đinh Mão')
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(1992, 5, 17, 6, 0)), 'Ất Mão')
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(2003, 12, 22, 6, 0)), 'Đinh Mão')
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(1990, 7, 10, 19, 0)), 'Mậu Tuất')
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(2002, 10, 24, 16, 28)), 'Giáp Thân')
        self.assertEqual(ZodiacUtil.zodiac_hour(Date(1991, 7, 3, 5, 50)), 'Đinh Mão')


if __name__ == '__main__':
    unittest.main()
