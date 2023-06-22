from functools import lru_cache
from math import floor, sin, cos, pi
from typing import Tuple, Union, List

from .date import Date, SolarDate, LunarDate
from .mixins import DateMixin, AngleMixin
from .exceptions import InvalidJulianDayException
from .tuvi.elements.nguhanh import NguHanh
from .tuvi.elements.can import Can
from .tuvi.elements.chi import Chi
from .localizer import VNLocalizer


class DateUtil(DateMixin, AngleMixin):
    """
    A class contains utility functions for date processing.
    """

    @staticmethod
    def get_day_of_the_week(date: SolarDate) -> str:
        """
        Compute weekday given `date`.
        """

        jd = DateUtil.jd_from_date(date)
        rem = int(round(jd + 1.5)) % 7
        weekdays = {
            0: 'Sunday',
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday'
        }

        return weekdays.get(rem)
    

    @staticmethod
    def get_day_of_the_year(date: SolarDate) -> int:
        """
        Compute day number of the year.
        """

        m, d = date.month, date.day
        if DateUtil.is_leap_year(date):
            k = 1
        else:
            k = 2

        return int(275 * m / 9) - k * int((m + 9) / 12) + d - 30


    @staticmethod
    def get_date_from_doty(year: int, doty: int) -> SolarDate:
        """
        Compute date given day of the year `doty` of `year`.
        """

        if DateUtil.is_leap_year(year):
            k = 1
        else:
            k = 2

        m = int(9 * (k + doty) / 275 + 0.98)
        if doty < 32:
            m = 1
        
        d = doty - int(275 * m / 9) + k * int((m + 9) / 12) + 30
        return SolarDate(year, m, d)


    @staticmethod
    @lru_cache(maxsize=1)
    def get_julian_date_threshold() -> Date:
        """
        Last Julian date is October 4th, 1582. Consider till 23:59, and this is for "<" comparison, 
        return October 5th, 1582 00:00 instead.
        """

        return Date(1582, 10, 5)


    @staticmethod
    def is_leap_year(param: Union[SolarDate, int]) -> bool:
        """
        Check if a given date's year is a leap year.
        """
        if isinstance(param, int):
            return (param % 4 == 0 and param % 100 != 0) or param % 400 == 0

        return (param.year % 4 == 0 and param.year % 100 != 0) or param.year % 400 == 0
    

    @staticmethod
    def decompose_fractional_day(fractional_day: float) -> Tuple[int, int, int, int]:
        """
        Decompose fractional day into integral day, hour, minute and second.
        For example, 2.5 days equals 2 days and 12 hours.
        """

        day = int(fractional_day)
        rem = fractional_day - day
        rem_seconds = int(round(rem * 86400))

        second = rem_seconds % 60
        minutes = rem_seconds // 60
        minute = minutes % 60
        hour = minutes // 60
        return day, hour, minute, second
    

    @staticmethod
    def get_fractional_day(date: Date) -> float:
        """
        Compute fractional day from given `date`.
        """

        elapsed_seconds = date.hour * 3600 + date.minute * 60 + date.second
        return date.day + elapsed_seconds / 86400


    @staticmethod
    def jd_from_date(date: Date) -> float:
        """
        Compute Julian day given calendar date `date`.
        """

        d, m, y = DateUtil.get_fractional_day(date), date.month, date.year
        if m <= 2:
            m += 12
            y -= 1

        a = int(floor(y / 100))
        b = 2 - a + int(floor(a / 4))

        # Check if date is Julian date
        if date < DateUtil.get_julian_date_threshold():
            b = 0

        jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5
        return jd
    

    @staticmethod
    def jd0_from_year(year: int) -> float:
        """
        Compute Julian day for given `year`, January 0.0 - the same as December 31.0 of the preceding year.
        """

        y = year - 1
        a = int(float(y / 100))
        return int(365.25 * y) - a + int(floor(a / 4)) + 1721424.5
    

    @staticmethod
    def mjd_from_date(date: Date) -> float:
        """
        Compute Modified Julian Day (MJD). MJD begins at Greenwich mean midnight.
        MJD = 0.0 corresponds to Novembere 17th, 1858 00:00 UTC+0.

        MJD = JD - 2400000.5
        """

        return DateUtil.jd_from_date(date) - 2400000.5
    

    @staticmethod
    def date_from_jd(jd: float) -> Date:
        """
        Compute calendar date from given Julian day `jd`.
        """

        if jd < 0:
            raise InvalidJulianDayException('Julian day cannot be negative.')
        
        z = int(jd + 0.5) # integral part of jd + 0.5
        f = jd + 0.5 - z # fractional part of jd + 0.5
        if z < 2299161:
            a = z
        else:
            alpha = int((z - 1867216.25) / 36524.25)
            a = z + 1 + alpha - int(floor(alpha / 4))
        
        b = a + 1524
        c = int(floor((b - 122.1) / 365.25))
        d = int(365.25 * c)
        e = int(floor((b - d) / 30.6001))

        fractional_day = b - d - int(30.6001 * e) + f
        day, hour, minute, second = DateUtil.decompose_fractional_day(fractional_day)

        if e < 14:
            month = e - 1
        else:
            month = e - 13
        
        if month > 2:
            year = c - 4716
        else:
            year = c - 4715

        return Date(year, month, day, hour, minute, second)


    @staticmethod
    def get_diff_days(date1: Date, date2: Date) -> float:
        """
        Compute the difference in days between two date `date1` and `date2`.
        """

        return abs(DateUtil.jd_from_date(date1) - DateUtil.jd_from_date(date2))


    @staticmethod
    def add_days(date: Date, days: Union[float, int]) -> Date:
        """
        Compute date after adding `days` days to date `date`.
        """
        return DateUtil.date_from_jd(DateUtil.jd_from_date(date) + days)
    
    
    @staticmethod
    def sub_days(date: Date, days: Union[float, int]) -> Date:
        """
        Compute date after subtracting `days` days to date `date`.
        """
        return DateUtil.date_from_jd(DateUtil.jd_from_date(date) - days)


    @staticmethod
    def _get_easter_sunday_gregorian(param: Union[SolarDate, int]) -> SolarDate:
        """
        Compute the Christian Easter Sunday of a given year. 
        This is the first Sunday after the Full Moon that happens on or next after the March equinox.

        Only valid for Gregorian calendar date.

        This method is marked as private. SHOULD NOT CALL THIS METHOD DIRECTLY.
        """

        if isinstance(param, Date):
            x = param.year
        else:
            x = param

        a = x % 19
        b = x // 100
        c = x % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (a * 19 + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + e * 2 + i * 2 - h - k) % 7
        m = (a + h * 11 + l * 22) // 451
        n = (h + l - m * 7 + 114) // 31
        p = (h + l - m * 7 + 114) % 31

        return Date(x, n, p + 1)
    
    
    @staticmethod
    def _get_easter_sunday_julian(param: Union[SolarDate, int]) -> SolarDate:
        """
        Compute the Christian Easter Sunday of a given year. 
        This is the first Sunday after the Full Moon that happens on or next after the March equinox.

        Only valid for Julian calendar date.

        This method is marked as private. SHOULD NOT CALL THIS METHOD DIRECTLY.
        """

        if isinstance(param, Date):
            x = param.year
        else:
            x = param

        a = x % 4
        b = x % 7
        c = x % 19
        d = (c * 19 + 15) % 30
        e = (a * 2 + b * 4 - d + 34) % 7
        f = (d + e + 114) // 31
        g = (d + e + 114) % 31

        return Date(x, f, g + 1)
    

    @staticmethod
    def get_easter_sunday(param: Union[SolarDate, int]) -> SolarDate:
        """
        Compute the Christian Easter Sunday of a given year. 
        This is the first Sunday after the Full Moon that happens on or next after the March equinox.
        """

        if isinstance(param, Date):
            x = param.year
        else:
            x = param

        if x <= 1582:
            return DateUtil._get_easter_sunday_julian(param)
        else:
            return DateUtil._get_easter_sunday_gregorian(param)
    

    @staticmethod
    @lru_cache
    def jde_of_kth_new_moon(k: int) -> float:
        """
        Compute the `k`-th new moon in Julian Ephemeris Day.
        `k` = 0 corresponds to the New Moon of 2000 January 6.
        """

        T = k / 1236.85 # time in Julian centuries since the epoch 2000
        jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * (T ** 2) - 0.000000150 * (T ** 3) + 0.00000000073 * (T ** 4) # need to correct
        E = 1 - 0.002516 * T - 0.0000074 * (T ** 2)

        # The following is computed at jde
        sun_mean_anomaly = 2.5534 + 29.10535670 * k - 0.0000014 * (T ** 2) - 0.00000011 * (T ** 3)
        moon_mean_anomaly = 201.5643 + 385.81693528 * k + 0.0107582 * (T ** 2) + 0.00001238 * (T ** 3) - 0.000000058 * (T ** 4)
        moon_arg_lat = 160.7108 + 390.67050284 * k - 0.0016118 * (T ** 2) - 0.00000227 * (T ** 3) + 0.000000011 * (T ** 4)
        long_asc_node = 124.7746 - 1.56375588 * k + 0.0020672 * (T ** 2) + 0.00000215 * (T ** 3)

        # Planetary arguments
        A1 = 299.77 + 0.107408 * k - 0.009173 * (T ** 2)
        A2 = 251.88 + 0.016321 * k
        A3 = 251.83 + 26.651886 * k
        A4 = 349.42 + 36.412478 * k
        A5 = 84.66 + 18.206239 * k
        A6 = 141.74 + 53.303771 * k
        A7 = 207.14 + 2.453732 * k
        A8 = 154.84 + 7.306860 * k
        A9 = 34.52 + 27.261239 * k
        A10 = 207.19 + 0.121824 * k
        A11 = 291.34 + 1.844379 * k
        A12 = 161.72 + 24.198154 * k
        A13 = 239.56 + 25.513099 * k
        A14 = 331.55 + 3.592518 * k

        first_correction = -0.40720 * sin(DateUtil.to_radians(moon_mean_anomaly)) + \
                            0.17241 * E * sin(DateUtil.to_radians(sun_mean_anomaly)) + \
                            0.01608 * sin(DateUtil.to_radians(2 * moon_mean_anomaly)) + \
                            0.01039 * sin(DateUtil.to_radians(2 * moon_arg_lat)) + \
                            0.00739 * E * sin(DateUtil.to_radians(moon_mean_anomaly - sun_mean_anomaly)) - \
                            0.00514 * E * sin(DateUtil.to_radians(moon_mean_anomaly + sun_mean_anomaly)) + \
                            0.00208 * (E ** 2) * sin(DateUtil.to_radians(2 * sun_mean_anomaly)) - \
                            0.00111 * sin(DateUtil.to_radians(moon_mean_anomaly - 2 * moon_arg_lat)) - \
                            0.00057 * sin(DateUtil.to_radians(moon_mean_anomaly + 2 * moon_arg_lat)) + \
                            0.00056 * E * sin(DateUtil.to_radians(moon_mean_anomaly * 2 + sun_mean_anomaly)) - \
                            0.00042 * sin(DateUtil.to_radians(moon_mean_anomaly * 3)) + \
                            0.00042 * E * sin(DateUtil.to_radians(sun_mean_anomaly + moon_arg_lat * 2)) + \
                            0.00038 * E * sin(DateUtil.to_radians(sun_mean_anomaly - moon_arg_lat * 2)) - \
                            0.00024 * E * sin(DateUtil.to_radians(moon_mean_anomaly * 2 - sun_mean_anomaly)) - \
                            0.00017 * sin(DateUtil.to_radians(long_asc_node)) - \
                            0.00007 * sin(DateUtil.to_radians(moon_mean_anomaly + sun_mean_anomaly * 2)) + \
                            0.00004 * sin(DateUtil.to_radians(moon_mean_anomaly * 2 - moon_arg_lat * 2)) + \
                            0.00004 * sin(DateUtil.to_radians(3 * sun_mean_anomaly)) + \
                            0.00003 * sin(DateUtil.to_radians(moon_mean_anomaly + sun_mean_anomaly - moon_arg_lat * 2)) + \
                            0.00003 * sin(DateUtil.to_radians(moon_mean_anomaly * 2 + moon_arg_lat * 2)) - \
                            0.00003 * sin(DateUtil.to_radians(moon_mean_anomaly + sun_mean_anomaly + moon_arg_lat * 2)) + \
                            0.00003 * sin(DateUtil.to_radians(moon_mean_anomaly - sun_mean_anomaly + moon_arg_lat * 2)) - \
                            0.00002 * sin(DateUtil.to_radians(moon_mean_anomaly - sun_mean_anomaly - moon_arg_lat * 2)) - \
                            0.00002 * sin(DateUtil.to_radians(moon_mean_anomaly * 3 + sun_mean_anomaly)) + \
                            0.00002 * sin(DateUtil.to_radians(moon_mean_anomaly * 4))
        
        second_correction = 0.000325 * sin(DateUtil.to_radians(A1)) + 0.000165 * sin(DateUtil.to_radians(A2)) + \
                            0.000164 * sin(DateUtil.to_radians(A3)) + 0.000126 * sin(DateUtil.to_radians(A4)) + \
                            0.000110 * sin(DateUtil.to_radians(A5)) + 0.000062 * sin(DateUtil.to_radians(A6)) + \
                            0.000060 * sin(DateUtil.to_radians(A7)) + 0.000056 * sin(DateUtil.to_radians(A8)) + \
                            0.000047 * sin(DateUtil.to_radians(A9)) + 0.000042 * sin(DateUtil.to_radians(A10)) + \
                            0.000040 * sin(DateUtil.to_radians(A11)) + 0.000037 * sin(DateUtil.to_radians(A12)) + \
                            0.000035 * sin(DateUtil.to_radians(A13)) + 0.000023 * sin(DateUtil.to_radians(A14))

        return jde + first_correction + second_correction


    @staticmethod
    def sun_longitude(jd: float) -> float:
        """
        Compute the longitude of sun given Julian day.
        """

        # Julian centuries
        T = (jd - 2451545) / 36525

        # Geometric mean longitude of the Sun, referred to the mean equinox of the date, in degree
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * (T ** 2)

        # Mean anomaly of the Sun, degree
        M = 357.52911 + 35999.05029 * T - 0.0001537 * (T ** 2)

        # Eccentricity of the Earth's orbit
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * (T ** 2)

        # Sun's equation of the center
        C = (1.914602 - 0.004817 * T - 0.000014 * (T ** 2)) * sin(DateUtil.to_radians(M)) + \
            (0.019993 - 0.000101 * T) * sin(DateUtil.to_radians(2 * M)) + \
            0.000289 * sin(DateUtil.to_radians(3 * M))

        # Sun's true longitude
        o = L0 + C

        # Sun's true anomaly
        v = M + C

        # Sun's radius vector, or the distance between the centers of the Sun and the Earth, expressed in astronomical units
        R = 1.000001018 * (1 - e ** 2) / (1 + e * cos(DateUtil.to_radians(v)))

        # Nutation and aberration correction
        ohm = 125.04 - 1934.136 * T

        # Apparent longitude
        lamb = o - 0.00569 - 0.00478 * sin(DateUtil.to_radians(ohm))

        return DateUtil.to_radians(lamb)

    
    @staticmethod
    def new_moon_tz_adjusted(k: int, timezone: int = 7) -> int:
        """
        Compute jde of `k`-th new moon with `timezone` adjusted.
        """

        return int(DateUtil.jde_of_kth_new_moon(k) + timezone / 24 + 0.5)
    

    @staticmethod
    def sun_longitude_tz_adjusted(jd: float, timezone: int = 7) -> int:
        """
        Compute sun longitude with `timezone` adjusted at given `jd`.
        Contract [0; 2*pi) to [0; 12) integer range.
        """
        return int(DateUtil.sun_longitude(jd - timezone / 24 - 0.5) / pi * 6)


    @staticmethod
    def get_lunar_month_11(param: Union[SolarDate, int], timezone: int = 7) -> int:
        """
        Find the first day of 11th month in lunar year.
        """
        
        if isinstance(param, Date):
            y = param.year
        else:
            y = param

        jd = DateUtil.jd_from_date(Date(y, 12, 31)) - DateUtil.jde_of_kth_new_moon(0) + 0.5
        k = int(floor(jd / 29.530588861))
        jd_kth_new_moon = DateUtil.new_moon_tz_adjusted(k, timezone)
        temp = DateUtil.sun_longitude_tz_adjusted(jd_kth_new_moon, timezone)
        
        if temp >= 9:
            jd_kth_new_moon = DateUtil.new_moon_tz_adjusted(k - 1, timezone)
        return jd_kth_new_moon


    @staticmethod
    def get_leap_month_offset(jd: float, timezone: int = 7) -> int:
        """
        Find the index of the next leap month after the month of the day `jd`.
        `jd` should be something like the result of `get_lunar_month_11` method.
        """
       
        k = int(floor((jd - DateUtil.jde_of_kth_new_moon(0)) / 29.530588861 + 0.5))
        last = 0
        i = 1  # start with month following 11th lunar month
        arc = DateUtil.sun_longitude_tz_adjusted(DateUtil.new_moon_tz_adjusted(k + i, timezone), timezone)

        while i < 14:
            last = arc
            i += 1
            arc = DateUtil.sun_longitude_tz_adjusted(DateUtil.new_moon_tz_adjusted(k + i, timezone), timezone)
            
            if arc == last:
                break
        
        return i - 1


    @staticmethod
    def solar_to_lunar(date: SolarDate, timezone: int = 7) -> LunarDate:
        """
        Convert solar date to lunar date at given `timezone`.
        """
        
        jd = DateUtil.jd_from_date(date) + 0.5
        k = int(floor((jd - DateUtil.jde_of_kth_new_moon(0)) / 29.530588861))
        jd_month_start = DateUtil.new_moon_tz_adjusted(k + 1, timezone)
        if jd_month_start > jd:
            jd_month_start = DateUtil.new_moon_tz_adjusted(k, timezone)

        a11 = DateUtil.get_lunar_month_11(date, timezone)
        b11 = a11
        if a11 >= jd_month_start:
            lunar_year = date.year
            a11 = DateUtil.get_lunar_month_11(date.year - 1, timezone)
        else:
            lunar_year = date.year + 1
            b11 = DateUtil.get_lunar_month_11(date.year + 1, timezone)

        lunar_day = int(jd - jd_month_start + 1)
        diff = int((jd_month_start - a11) / 29)
        lunar_month = diff + 11

        if b11 - a11 > 365:
            leap_month_diff = DateUtil.get_leap_month_offset(a11, timezone)
            if diff >= leap_month_diff:
                lunar_month = diff + 10
            
        if lunar_month > 12:
            lunar_month = lunar_month - 12
        if lunar_month >= 11 and diff < 4:
            lunar_year -= 1
        
        return Date(lunar_year, lunar_month, lunar_day)


    @staticmethod
    def lunar_to_solar(date: LunarDate, timezone: int = 7) -> SolarDate:
        """
        Convert lunar date to solar date at given `timezone`.
        """

        if date.month < 11:
            a11 = DateUtil.get_lunar_month_11(date.year - 1, timezone)
            b11 = DateUtil.get_lunar_month_11(date.year, timezone)
        else:
            a11 = DateUtil.get_lunar_month_11(date.year, timezone)
            b11 = DateUtil.get_lunar_month_11(date.year + 1, timezone)

        k = int(floor((a11 - DateUtil.jde_of_kth_new_moon(0)) / 29.530588861 + 0.5))
        off = date.month - 11

        if off < 0:
            off += 12

        if b11 - a11 > 365:
            leap_off = DateUtil.get_leap_month_offset(a11, timezone)   
            leap_month = leap_off - 2         

            if leap_month < 0:
                leap_month += 12

            if DateUtil.is_leap_lunar_year(date) and date.month != leap_month:
                if off >= leap_off:
                    off += 1
            elif DateUtil.is_leap_lunar_year(date) or off >= leap_off:
                off += 1

        jde_month_start = DateUtil.new_moon_tz_adjusted(k + off, timezone)
        return DateUtil.date_from_jd(jde_month_start + date.day - 1 - 0.5).empty_hms()


    @staticmethod
    def is_leap_lunar_year(param: Union[LunarDate, int]) -> bool:
        """
        Check if the given year is a leap year in lunar calendar.
        """
        if isinstance(param, Date):
            y = param.year
        else:
            y = param

        return y % 19 in [0, 3, 6, 9, 11, 14, 17]
    

class NguHanhUtil:
    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_tuong_sinh(nguhanh: int) -> List[int]:
        """
        Lay list cac hanh tuong sinh voi `nguhanh`.
        """

        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return [NguHanh.THUY, NguHanh.THO]
        if nguhanh == NguHanh.MOC:
            return [NguHanh.THUY, NguHanh.HOA]
        if nguhanh == NguHanh.THUY:
            return [NguHanh.MOC, NguHanh.KIM]
        if nguhanh == NguHanh.HOA:
            return [NguHanh.MOC, NguHanh.THO]
        if nguhanh == NguHanh.THO:
            return [NguHanh.HOA, NguHanh.KIM]
        
        return []
    
    
    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_sinh_cho(nguhanh: int) -> int:
        """
        Tim hanh sinh cho ngu hanh `nguhanh`.
        """
        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return NguHanh.THO
        if nguhanh == NguHanh.MOC:
            return NguHanh.THUY
        if nguhanh == NguHanh.THUY:
            return NguHanh.KIM
        if nguhanh == NguHanh.HOA:
            return NguHanh.MOC
        if nguhanh == NguHanh.THO:
            return NguHanh.HOA
        
        return None
        

    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_duoc_sinh(nguhanh: int) -> int:
        """
        Tim ngu hanh ma `nguhanh` sinh cho.
        """

        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return NguHanh.THUY
        if nguhanh == NguHanh.MOC:
            return NguHanh.HOA
        if nguhanh == NguHanh.THUY:
            return NguHanh.MOC
        if nguhanh == NguHanh.HOA:
            return NguHanh.THO
        if nguhanh == NguHanh.THO:
            return NguHanh.KIM
        
        return None

    
    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_tuong_khac(nguhanh: int) -> List[int]:
        """
        Lay list cac hanh ma tuong khac voi `nguhanh`.
        """

        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return [NguHanh.HOA, NguHanh.MOC]
        if nguhanh == NguHanh.MOC:
            return [NguHanh.KIM, NguHanh.THO]
        if nguhanh == NguHanh.THUY:
            return [NguHanh.HOA, NguHanh.THO]
        if nguhanh == NguHanh.HOA:
            return [NguHanh.THUY, NguHanh.KIM]
        if nguhanh == NguHanh.THO:
            return [NguHanh.THUY, NguHanh.MOC]
        
        return []
    
    
    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_khac_che(nguhanh: int) -> int:
        """
        Tim hanh khac che `nguhanh`.
        """

        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return NguHanh.HOA
        if nguhanh == NguHanh.MOC:
            return NguHanh.KIM
        if nguhanh == NguHanh.THUY:
            return NguHanh.THO
        if nguhanh == NguHanh.HOA:
            return NguHanh.THUY
        if nguhanh == NguHanh.THO:
            return NguHanh.MOC
        
        return None
        

    @staticmethod
    @lru_cache(maxsize=10)
    def get_ngu_hanh_bi_khac(nguhanh: int) -> int:
        """
        Tim hanh bi `nguhanh` khac che.
        """

        if nguhanh is None:
            return None
        
        if nguhanh == NguHanh.KIM:
            return NguHanh.MOC
        if nguhanh == NguHanh.MOC:
            return NguHanh.THO
        if nguhanh == NguHanh.THUY:
            return NguHanh.HOA
        if nguhanh == NguHanh.HOA:
            return NguHanh.KIM
        if nguhanh == NguHanh.THO:
            return NguHanh.THUY
        
        return None
    

    @staticmethod
    @lru_cache(maxsize=40)
    def check_tuong_sinh(nguhanh1: int, nguhanh2: int) -> bool:
        """
        Tra ve True neu `nguhanh1` va `nguhanh2` tuong sinh.
        """

        return nguhanh2 in NguHanhUtil.get_ngu_hanh_tuong_sinh(nguhanh1)
    

    @staticmethod
    @lru_cache(maxsize=40)
    def check_tuong_khac(nguhanh1: int, nguhanh2: int) -> bool:
        """
        Tra ve True neu `nguhanh1` va `nguhanh2` tuong khac.
        """

        return nguhanh2 in NguHanhUtil.get_ngu_hanh_tuong_khac(nguhanh1)


    @staticmethod
    @lru_cache(maxsize=10)
    def ngu_hanh_from_string(nguhanh: str) -> int:
        temp_dict = {
            'Kim': NguHanh.KIM,
            'Mộc': NguHanh.MOC,
            'Thuỷ': NguHanh.THUY,
            'Hoả': NguHanh.HOA,
            'Thổ': NguHanh.THO,
        }

        return temp_dict.get(nguhanh)


class ZodiacUtil:
    @staticmethod
    @VNLocalizer.localizer
    def zodiac_year(date: Date) -> str:
        """
        Return zodiac year for given `date`.
        """

        can_index = (date.year + 6) % 10 + 1
        chi_index = (date.year + 8) % 12 + 1
        return '{} {}'.format(Can(can_index).name.capitalize(), Chi(chi_index).name.capitalize())


    @staticmethod
    @VNLocalizer.localizer
    def zodiac_month(date: Date) -> str:
        """
        Return zodiac month for given `date`.
        """

        can_index = (date.year * 12 + date.month + 3) % 10 + 1
        return '{} {}'.format(Can(can_index).name.capitalize(), Chi((date.month + 1) % 12 + 1).name.capitalize())
    

    @staticmethod
    @VNLocalizer.localizer
    def zodiac_day(date: Date) -> str:
        """
        Return zodiac day for given `date`. Must be an empty_hms() date.

        NOTE: `date` must be a solar date, not a lunar date.
        """

        jd = int(round(DateUtil.jd_from_date(date.empty_hms()) + 0.5))
        can_index = (jd + 9) % 10 + 1
        chi_index = (jd + 1) % 12 + 1
        return '{} {}'.format(Can(can_index).name.capitalize(), Chi(chi_index).name.capitalize())


    @staticmethod
    @VNLocalizer.localizer
    def zodiac_hour(date: Date) -> str:
        """
        Return zodiac hour for given `date`. Must be an empty_hms() date.

        NOTE: `date` must be a solar date, not a lunar date.
        """
        
        if date.hour == 23 or date.hour == 0:
            chi_index = 1
        else:
            chi_index = (date.hour - 1) // 2 + 2
        
        
        jd = int(round(DateUtil.jd_from_date(date.empty_hms()) + 0.5))
        can_index_day = (jd + 9) % 10 + 1
        can_index = (2 * ((can_index_day - 1) % 5) + chi_index - 1) % 10 + 1

        return '{} {}'.format(Can(can_index).name.capitalize(), Chi(chi_index).name.capitalize())
    

    @staticmethod
    def zodiac_year_tuple(date: Date) -> Tuple[int, int]:
        """
        Return zodiac year for given `date` in form of an index tuple.
        """

        can_index = (date.year + 6) % 10 + 1
        chi_index = (date.year + 8) % 12 + 1
        return can_index, chi_index


    @staticmethod
    def zodiac_month_tuple(date: Date) -> Tuple[int, int]:
        """
        Return zodiac month for given `date` in form of an index tuple.
        """

        can_index = (date.year * 12 + date.month + 3) % 10 + 1
        chi_index = (date.month + 1) % 12 + 1
        return can_index, chi_index
    

    @staticmethod
    def zodiac_day_tuple(date: Date) -> Tuple[int, int]:
        """
        Return zodiac day for given `date` in form of an index tuple. Must be an empty_hms() date.

        NOTE: `date` must be a solar date, not a lunar date.
        """

        jd = int(round(DateUtil.jd_from_date(date.empty_hms()) + 0.5))
        can_index = (jd + 9) % 10 + 1
        chi_index = (jd + 1) % 12 + 1
        return can_index, chi_index


    @staticmethod
    def zodiac_hour_tuple(date: Date) -> Tuple[int, int]:
        """
        Return zodiac hour for given `date` in form of an index tuple.

        NOTE: `date` must be a solar date, not a lunar date.
        """
        
        if date.hour == 23 or date.hour == 0:
            chi_index = 1
        else:
            chi_index = (date.hour - 1) // 2 + 2
        
        
        jd = int(round(DateUtil.jd_from_date(date.empty_hms()) + 0.5))
        can_index_day = (jd + 9) % 10 + 1
        can_index = (2 * ((can_index_day - 1) % 5) + chi_index - 1) % 10 + 1
        return can_index, chi_index
