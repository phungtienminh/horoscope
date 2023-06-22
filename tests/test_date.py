import unittest

from core.date import Date
from core.utils import DateUtil


class TestDate(unittest.TestCase):
    def test_julian_day(self):
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1999, 1, 1)), 2451179.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1987, 1, 27)), 2446822.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1988, 1, 27)), 2447187.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1900, 1, 1)), 2415020.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1600, 1, 1)), 2305447.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(1600, 12, 31)), 2305812.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(-123, 12, 31)), 1676496.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(-122, 1, 1)), 1676497.5)
        self.assertAlmostEqual(DateUtil.jd_from_date(Date(-1000, 2, 29)), 1355866.5)


    def test_leap_year(self):
        self.assertEqual(DateUtil.is_leap_year(Date(2000, 3, 5)), True)
        self.assertEqual(DateUtil.is_leap_year(Date(2002, 3, 5)), False)
        self.assertEqual(DateUtil.is_leap_year(Date(1900, 3, 5)), False)
        self.assertEqual(DateUtil.is_leap_year(Date(2003, 3, 5)), False)
        self.assertEqual(DateUtil.is_leap_year(Date(2023, 3, 5)), False)
        self.assertEqual(DateUtil.is_leap_year(Date(2016, 2, 29)), True)


    def test_decompose_fractional_day(self):
        self.assertEqual(DateUtil.decompose_fractional_day(4.81), (4, 19, 26, 24))
        self.assertEqual(DateUtil.decompose_fractional_day(0.63), (0, 15, 7, 12))
        self.assertEqual(DateUtil.decompose_fractional_day(2.5), (2, 12, 0, 0))


    def test_fractional_day(self):
        self.assertAlmostEqual(DateUtil.get_fractional_day(Date(day=4, hour=19, minute=26, second=24)), 4.81)


    def test_reverse_julian_day(self):
        self.assertEqual(DateUtil.date_from_jd(2436116.31), Date(1957, 10, 4, 19, 26, 24))
        self.assertEqual(DateUtil.date_from_jd(1842713), Date(333, 1, 27, 12, 0, 0))
        self.assertEqual(DateUtil.date_from_jd(1507900.13), Date(-584, 5, 28, 15, 7, 12))


    def test_date_diff(self):
        self.assertAlmostEqual(DateUtil.get_diff_days(Date(1910, 4, 20), Date(1986, 2, 9)), 27689.0)
    
    
    def test_add_date(self):
        self.assertEqual(DateUtil.add_days(Date(1991, 7, 11), 10000), Date(2018, 11, 26))

    
    def test_sub_date(self):
        self.assertEqual(DateUtil.sub_days(Date(2018, 11, 26), 10000), Date(1991, 7, 11))

    
    def test_weekday(self):
        self.assertEqual(DateUtil.get_day_of_the_week(Date(1954, 6, 30)), 'Wednesday')
        self.assertEqual(DateUtil.get_day_of_the_week(Date(2023, 6, 12)), 'Monday')

    
    def test_doty(self):
        self.assertEqual(DateUtil.get_day_of_the_year(Date(1978, 11, 14)), 318)
        self.assertEqual(DateUtil.get_day_of_the_year(Date(1988, 4, 22)), 113)

    
    def test_date_from_doty(self):
        self.assertEqual(DateUtil.get_date_from_doty(1978, 318), Date(1978, 11, 14))
        self.assertEqual(DateUtil.get_date_from_doty(1988, 113), Date(1988, 4, 22))

    
    def test_easter_sunday(self):
        self.assertEqual(DateUtil.get_easter_sunday(1991), Date(1991, 3, 31))
        self.assertEqual(DateUtil.get_easter_sunday(1992), Date(1992, 4, 19))
        self.assertEqual(DateUtil.get_easter_sunday(1993), Date(1993, 4, 11))
        self.assertEqual(DateUtil.get_easter_sunday(1954), Date(1954, 4, 18))
        self.assertEqual(DateUtil.get_easter_sunday(2000), Date(2000, 4, 23))
        self.assertEqual(DateUtil.get_easter_sunday(1818), Date(1818, 3, 22))


    def test_new_moon(self):
        self.assertAlmostEqual(DateUtil.jde_of_kth_new_moon(-283), 2443192.65118, places=5)

    
    def test_sun_longitude(self):
        self.assertAlmostEqual(DateUtil.sun_longitude(2448908.5), DateUtil.to_radians(199 + 54 / 60 + 21.56 / 3600), places=3)


    def test_solar_to_lunar(self):
        # 1st batch
        self.assertEqual(DateUtil.solar_to_lunar(Date(2023, 6, 13)), Date(2023, 4, 26))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2002, 3, 22)), Date(2002, 2, 9))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2006, 1, 8)), Date(2005, 12, 9))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1996, 8, 4)), Date(1996, 6, 21))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1995, 8, 9)), Date(1995, 7, 14))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1977, 4, 24)), Date(1977, 3, 7))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2002, 12, 1)), Date(2002, 10, 27))

        # 2nd batch
        self.assertEqual(DateUtil.solar_to_lunar(Date(1967, 12, 10)), Date(1967, 11, 10))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1988, 2, 15)), Date(1987, 12, 28))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1996, 6, 19)), Date(1996, 5, 4))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1994, 11, 4)), Date(1994, 10, 2))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1998, 10, 20)), Date(1998, 9, 1))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1991, 7, 26)), Date(1991, 6, 15))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1999, 2, 4)), Date(1998, 12, 19))

        # 3rd batch
        self.assertEqual(DateUtil.solar_to_lunar(Date(2000, 10, 18)), Date(2000, 9, 21))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1961, 5, 5)), Date(1961, 3, 21))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2004, 12, 5)), Date(2004, 10, 24))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2022, 4, 13)), Date(2022, 3, 13))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1987, 2, 19)), Date(1987, 1, 22))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2012, 2, 20)), Date(2012, 1, 29))
        self.assertEqual(DateUtil.solar_to_lunar(Date(2014, 4, 4)), Date(2014, 3, 5))
        self.assertEqual(DateUtil.solar_to_lunar(Date(1990, 7, 10)), Date(1990, 5, 18))


    def test_lunar_to_solar(self):
        # 1st batch
        self.assertEqual(DateUtil.lunar_to_solar(Date(2023, 4, 26)), Date(2023, 6, 13))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2002, 2, 9)), Date(2002, 3, 22))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2005, 12, 9)), Date(2006, 1, 8))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1996, 6, 21)), Date(1996, 8, 4))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1995, 7, 14)), Date(1995, 8, 9))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1977, 3, 7)), Date(1977, 4, 24))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2002, 10, 27)), Date(2002, 12, 1))

        # 2nd batch
        self.assertEqual(DateUtil.lunar_to_solar(Date(1967, 11, 10)), Date(1967, 12, 10))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1987, 12, 28)), Date(1988, 2, 15))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1996, 5, 4)), Date(1996, 6, 19))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1994, 10, 2)), Date(1994, 11, 4))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1998, 9, 1)), Date(1998, 10, 20))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1991, 6, 15)), Date(1991, 7, 26))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1998, 12, 19)), Date(1999, 2, 4))

        # 3rd batch
        self.assertEqual(DateUtil.lunar_to_solar(Date(2000, 9, 21)), Date(2000, 10, 18))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1961, 3, 21)), Date(1961, 5, 5))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2004, 10, 24)), Date(2004, 12, 5))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2022, 3, 13)), Date(2022, 4, 13))
        self.assertEqual(DateUtil.lunar_to_solar(Date(1987, 1, 22)), Date(1987, 2, 19))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2012, 1, 29)), Date(2012, 2, 20))
        self.assertEqual(DateUtil.lunar_to_solar(Date(2014, 3, 5)), Date(2014, 4, 4))


if __name__ == '__main__':
    unittest.main()
