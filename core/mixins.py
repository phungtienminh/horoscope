from functools import lru_cache
from typing import Union
from math import pi

from .exceptions import InvalidMonthException


class DateMixin:
    @staticmethod
    @lru_cache(maxsize=35)
    def get_ordinal(number: int) -> str:
        """
        Get ordinal suffix of number in range [1, 31].
        """

        if number in [1, 21, 31]:
            return f'{number}st'
        if number in [2, 22]:
            return f'{number}nd'
        if number in [3, 23]:
            return f'{number}rd'
        
        return f'{number}th'


    @staticmethod
    @lru_cache(maxsize=25)
    def days_of_month(month: int, leap: bool = False) -> int:
        """
        Get the number of days in month `month`.
        """

        if leap and month == 2:
            return 29
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month == 2:
            return 28
        return 30
    

    @staticmethod
    @lru_cache(maxsize=15)
    def get_month_name(month: int) -> str:
        """
        Get the month name given `month`, i.e, 1 to January.
        """

        if not 1 <= month <= 12:
            raise InvalidMonthException('Invalid month.')

        month_to_name_dict = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        
        return month_to_name_dict.get(month)
    

class AngleMixin:
    @staticmethod
    def to_radians(degrees: Union[float, int]) -> float:
        result = degrees * pi / 180.0
        while result >= 2 * pi:
            result -= 2 * pi
        while result < 0:
            result += 2 * pi

        return result
    
    
    @staticmethod
    def to_degrees(radians: Union[float, int]) -> float:
        return radians * 180.0 / pi
