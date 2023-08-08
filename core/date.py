from __future__ import annotations

from .exceptions import InvalidDateException
from .mixins import DateMixin


class Date(DateMixin):
    """
    Date class.
    """

    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, second: int = 0) -> None:
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second


    @property
    def year(self) -> int:
        return self._year
    

    @year.setter
    def year(self, new_year: int) -> None:
        self._year = new_year


    @property
    def month(self) -> int:
        return self._month
    

    @month.setter
    def month(self, new_month: int) -> None:
        if not 1 <= new_month <= 12:
            raise InvalidDateException('Invalid month')

        self._month = new_month


    @property
    def day(self) -> int:
        return self._day
    

    @day.setter
    def day(self, new_day: int) -> None:
        if self.month == 2:
            if self.is_leap_year(self):
                if not 1 <= new_day <= 29:
                    raise InvalidDateException('Invalid day')
            else:
                if not 1 <= new_day <= 28:
                    raise InvalidDateException('Invalid day')
        else:
            if not 1 <= new_day <= self.days_of_month(self.month):
                raise InvalidDateException('Invalid day')
            
        self._day = new_day

    
    @property
    def hour(self) -> int:
        return self._hour
    

    @hour.setter
    def hour(self, new_hour: int) -> None:
        self._hour = new_hour


    @property
    def minute(self) -> int:
        return self._minute
    
    
    @minute.setter
    def minute(self, new_minute: int) -> None:
        self._minute = new_minute

    
    @property
    def second(self) -> int:
        return self._second
    

    @second.setter
    def second(self, new_second: int) -> None:
        self._second = new_second


    def empty_hms(self) -> Date:
        """
        Reset hour, minute and second to zero.
        """
        
        return Date(self.year, self.month, self.day)

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return self.second < other.second


    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day and self.hour == other.hour and self.minute == other.minute and self.second == other.second
    

    def __gt__(self, other):
        return other < self

    
    def __le__(self, other):
        return self < other or self == other
    

    def __ge__(self, other):
        return self > other or self == other
    

    def __ne__(self, other):
        return self.year != other.year or self.month != other.month or self.day != other.day or self.hour != other.hour or self.minute != other.minute or self.second != other.second


    def __str__(self):
        return f'{self.get_month_name(self.month)} {self.get_ordinal(self.day)}, {self.year} {str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}'


    def __repr__(self):
        return f'{self.get_month_name(self.month)} {self.get_ordinal(self.day)}, {self.year} {str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}'
    

    def __hash__(self):
        return hash((self.year, self.month, self.day, self.hour, self.minute, self.second))


class SolarDate(Date):
    """
    Class for solar date, a subclass of Date.
    """
    pass


class LunarDate(Date):
    """
    Class for lunar date, a subclass of Date.
    """
    pass
