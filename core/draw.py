from enum import Enum
from typing import Union, Tuple
from .exceptions import InvalidPercentValue, InvalidID
from core.tuvi.elements.nguhanh import NguHanh


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (28, 128, 19)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = (250, 241, 215)
    YELLOW = (209, 206, 15)
    GREY = (145, 144, 134)


class FontSize(Enum):
    SMALL = 11
    MEDIUM = 12
    LARGE = 14


def get_position(topleft: Tuple[int, int], size: Tuple[int, int], width: Union[float, None] = None, height: Union[float, None] = None, width_percent: Union[float, None] = None, height_percent: Union[float, None] = None) -> Tuple[int, int]:
    if width_percent is not None and not 0 <= width_percent <= 100:
        raise InvalidPercentValue('Percent value must be between 0 and 100.')
    if height_percent is not None and not 0 <= height_percent <= 100:
        raise InvalidPercentValue('Percent value must be between 0 and 100.')
    
    if width is None and width_percent is None:
        raise Exception('Either fixed width or percentage width must be specified.')
    if width is not None and width_percent is not None:
        raise Exception('Only fixed width or percentage width can be set.')
    if height is None and height_percent is None:
        raise Exception('Either fixed height or percentage height must be specified.')
    if height is not None and height_percent is not None:
        raise Exception('Only fixed height or percentage height can be set.')
    
    x, y = topleft
    w, h = size

    if width is not None:
        if height is not None:
            return int(round(x + width)), int(round(y + height))
        else:
            return int(round(x + width)), int(round(y + h * height_percent / 100))
    else:
        if height is not None:
            return int(round(x + w * width_percent / 100)), int(round(y + height))
        else:
            return int(round(x + w * width_percent / 100)), int(round(y + h * height_percent / 100))


def get_color(ID: int) -> Tuple[int, int, int]:
    if not 1 <= ID <= 12:
        raise InvalidID('ID must be between 1 and 12.')
    
    if ID in [2, 5, 8, 11]:
        return Color.YELLOW.value
    if ID in [1, 12]:
        return Color.BLACK.value
    if ID in [3, 4]:
        return Color.GREEN.value
    if ID in [6, 7]:
        return Color.RED.value
    if ID in [9, 10]:
        return Color.GREY.value
    
    # Should never reach here
    return Color.WHITE.value


def get_color_by_nguhanh(nguhanh: int) -> Tuple[int, int, int]:
    if nguhanh == NguHanh.HOA.value:
        return Color.RED.value
    if nguhanh == NguHanh.THUY.value:
        return Color.BLACK.value
    if nguhanh == NguHanh.MOC.value:
        return Color.GREEN.value
    if nguhanh == NguHanh.THO.value:
        return Color.YELLOW.value
    if nguhanh == NguHanh.KIM.value:
        return Color.GREY.value
    
    # Should never reach here
    return Color.WHITE.value
