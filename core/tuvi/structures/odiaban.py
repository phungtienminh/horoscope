from core.exceptions import InvalidID, InvalidLoaiSao
from core.tuvi.stars.sao import Sao
from core.tuvi.elements.loaisao import LoaiSao

from typing import Union, List

class ODiaBan:
    def __init__(self, ID: int) -> None:
        if not 1 <= ID <= 12:
            raise InvalidID('ID must be between 1 and 12.')

        # Generic info
        self.ID: int = ID
        self.name: Union[str, None] = None # top middle
        self.cung_than: bool = False # top middle

        # 4 angles
        self.zodiac: Union[str, None] = None # top left
        self.dai_han: Union[int, None] = None # top right
        self.tieu_han: Union[str, None] = None # bottom left
        self.nguyet_han: Union[str, None] = None # bottom right

        # Stars
        self.chinh_tinh: List[Sao] = [] # top middle
        self.phu_tinh_trai: List[Sao] = [] # left
        self.phu_tinh_phai: List[Sao] = [] # right
        self.phu_tinh_duoi: Union[Sao, None] = None # only 1

        # For print

        # Map ID to paper coordinate
        temp = {
            1: (3, 2),
            2: (3, 1),
            3: (3, 0),
            4: (2, 0),
            5: (1, 0),
            6: (0, 0),
            7: (0, 1),
            8: (0, 2),
            9: (0, 3),
            10: (1, 3),
            11: (2, 3),
            12: (3, 3),
        }

        # Paper coordinate
        self.coor = temp[ID]


    def add_star(self, star: Sao) -> None:
        """
        Them sao vao o dia ban.
        """
        if star.loai_sao.value == LoaiSao.CHINH_TINH.value:
            self.chinh_tinh.append(star)
        elif star.loai_sao.value == LoaiSao.PHU_TINH_TRAI.value:
            self.phu_tinh_trai.append(star)
        elif star.loai_sao.value == LoaiSao.PHU_TINH_PHAI.value:
            self.phu_tinh_phai.append(star)
        elif star.loai_sao.value == LoaiSao.PHU_TINH_DUOI.value:
            self.phu_tinh_duoi = star
        else:
            raise InvalidLoaiSao('Loai sao khong hop le.')
        
