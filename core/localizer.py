from typing import Callable, Any
from abc import ABC, abstractmethod
from functools import lru_cache


class Localizer(ABC):
    @staticmethod
    @abstractmethod
    def localizer(f: Callable[..., str]) -> Callable[..., str]:
        """
        Generic decorator. To be overrided in subclasses.
        """
        pass


    @staticmethod
    @abstractmethod
    def _localize(s: str) -> str:
        """
        Localize a string.
        """
        pass


class VNLocalizer(Localizer):
    @staticmethod
    def localizer(f: Callable[..., str]) -> Callable[..., str]:
        def wrapper(*args: Any, **kwargs: Any) -> str:
            result = f(*args, **kwargs)
            return ' '.join(list(map(lambda token: VNLocalizer._localize(token), result.split())))

        return wrapper
    

    @staticmethod
    @lru_cache(maxsize=25)
    def _localize(s: str) -> str:
        """
        Vietnamese localizing a string.
        """

        d = {
            'Giap': 'Giáp',
            'At': 'Ất',
            'Binh': 'Bính',
            'Dinh': 'Đinh',
            'Mau': 'Mậu',
            'Ky': 'Kỷ',
            'Canh': 'Canh',
            'Tan': 'Tân',
            'Nham': 'Nhâm',
            'Quy': 'Quý',
            'Ti': 'Tí',
            'Suu': 'Sửu',
            'Dan': 'Dần',
            'Mao': 'Mão',
            'Thin': 'Thìn',
            'Ty': 'Tỵ',
            'Ngo': 'Ngọ',
            'Mui': 'Mùi',
            'Than': 'Thân',
            'Dau': 'Dậu',
            'Tuat': 'Tuất',
            'Hoi': 'Hợi',
        }

        return d.get(s)
