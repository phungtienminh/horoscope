from abc import ABC, abstractmethod
from typing import Tuple, Union, List
from functools import lru_cache

from core.date import Date, LunarDate, SolarDate
from core.tuvi.elements.amduong import AmDuong
from core.tuvi.elements.nguhanh import NguHanh
from core.tuvi.elements.trangthai import TrangThai
from core.tuvi.elements.loaisao import LoaiSao
from core.tuvi.elements.gioitinh import GioiTinh
from core.tuvi.utils import TuViUtil, ZodiacUtil
from core.utils import DateUtil
from core.exceptions import InvalidCuc, InvalidDayException, InvalidViTri


class Sao(ABC):
    name = None
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.NONE
    order = None
    is_print_bold = False


    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        SaoRegistry.register(cls)


    @staticmethod
    @abstractmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        """
        Given date of birth `birthdate` and generated year `cur_year`, return the position of this star
        as the ID of cell which contains the star.
        """
        pass


class SaoRegistry:
    _subclasses = []

    @classmethod
    def register(cls, subclass: Sao) -> None:
        """
        Add a subclass to the list of registered subclasses.
        """
        cls._subclasses.append(subclass)

    
    @classmethod
    def get_subclasses(cls) -> List[Sao]:
        """
        Return the list of registered subclasses.
        """
        return cls._subclasses


class SaoTuVi(Sao):
    name = "Tử Vi"
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True
    
    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        cuc = TuViUtil.tim_cuc(birthdate)
        day = lunar_date.day

        if cuc == 'Thuỷ nhị cục':
            if day in [22, 23]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 1
            if day in [1, 24, 25]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 2
            if day in [2, 3, 26, 27]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 3
            if day in [4, 5, 28, 29]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 4
            if day in [6, 7, 30]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 5
            if day in [8, 9]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 6
            if day in [10, 11]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 7
            if day in [12, 13]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 8
            if day in [14, 15]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 9
            if day in [16, 17]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 10
            if day in [18, 19]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 11
            if day in [20, 21]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 12
            
            raise InvalidDayException('Invalid day.')

        elif cuc == 'Mộc tam cục':
            if day in [25]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 1
            if day in [2, 28]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 2
            if day in [3, 5]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 3
            if day in [6, 8]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 4
            if day in [1, 9, 11]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 5
            if day in [4, 12, 14]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 6
            if day in [7, 15, 17]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 7
            if day in [10, 18, 20]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 8
            if day in [13, 21, 23]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 9
            if day in [16, 24, 26]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 10
            if day in [19, 27, 29]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 11
            if day in [22, 30]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 12
            
            raise InvalidDayException('Invalid day.')
        elif cuc == 'Kim tứ cục':
            if day in [5]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 1
            if day in [3, 9]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 2
            if day in [4, 7, 13]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 3
            if day in [8, 11, 17]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 4
            if day in [2, 12, 15, 21]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 5
            if day in [6, 16, 19, 25]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 6
            if day in [10, 20, 23, 29]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 7
            if day in [14, 24, 27]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 8
            if day in [18, 28]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 9
            if day in [22]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 10
            if day in [26]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 11
            if day in [1, 30]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 12
            
            raise InvalidDayException('Invalid day.')
        elif cuc == 'Thổ ngũ cục':
            if day in [7]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 1
            if day in [4, 12]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 2
            if day in [5, 9, 17]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 3
            if day in [10, 14, 22]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 4
            if day in [3, 15, 19, 27]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 5
            if day in [8, 20, 24]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 6
            if day in [1, 13, 25, 29]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 7
            if day in [6, 18, 30]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 8
            if day in [11, 23]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 9
            if day in [16, 28]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 10
            if day in [21]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 11
            if day in [2, 26]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 12
            
            raise InvalidDayException('Invalid day.')
        elif cuc == 'Hoả lục cục':
            if day in [9, 19]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 1
            if day in [5, 15, 25]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 2
            if day in [6, 11, 21]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 3
            if day in [12, 17, 27]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 4
            if day in [4, 18, 23]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 5
            if day in [10, 24, 29]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 6
            if day in [2, 16, 30]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 7
            if day in [8, 22]:
                SaoTuVi.trang_thai = TrangThai.DAC
                return 8
            if day in [14, 28]:
                SaoTuVi.trang_thai = TrangThai.MIEU
                return 9
            if day in [1, 20]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 10
            if day in [7, 26]:
                SaoTuVi.trang_thai = TrangThai.VUONG
                return 11
            if day in [3, 13]:
                SaoTuVi.trang_thai = TrangThai.BINH
                return 12
            
            raise InvalidDayException('Invalid day.')
        else:
            raise InvalidCuc('Cuc khong hop le.')
        

class SaoThienCo(Sao):
    name = 'Thiên Cơ'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tu_vi = SaoTuVi.an_sao(birthdate, cur_year)
        vi_tri_thien_co = (vi_tri_tu_vi - 2 + 12) % 12 + 1
        
        if vi_tri_thien_co in [4, 5, 10, 11]:
            SaoThienCo.trang_thai = TrangThai.MIEU
        elif vi_tri_thien_co in [6, 9]:
            SaoThienCo.trang_thai = TrangThai.VUONG
        elif vi_tri_thien_co in [1, 2, 7, 8]:
            SaoThienCo.trang_thai = TrangThai.DAC
        elif vi_tri_thien_co in [3, 12]:
            SaoThienCo.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_co
    

class SaoThaiDuong(Sao):
    name = 'Thái Dương'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_co = SaoThienCo.an_sao(birthdate, cur_year)
        vi_tri_thai_duong = (vi_tri_thien_co - 3 + 12) % 12 + 1
        
        if vi_tri_thai_duong in [6, 7]:
            SaoThaiDuong.trang_thai = TrangThai.MIEU
        elif vi_tri_thai_duong in [3, 4, 5]:
            SaoThaiDuong.trang_thai = TrangThai.VUONG
        elif vi_tri_thai_duong in [2, 8]:
            SaoThaiDuong.trang_thai = TrangThai.DAC
        elif vi_tri_thai_duong in [1, 9, 10, 11, 12]:
            SaoThaiDuong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thai_duong
    

class SaoVuKhuc(Sao):
    name = 'Vũ Khúc'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thai_duong = SaoThaiDuong.an_sao(birthdate, cur_year)
        vi_tri_vu_khuc = (vi_tri_thai_duong - 2 + 12) % 12 + 1

        if vi_tri_vu_khuc in [2, 5, 8, 11]:
            SaoVuKhuc.trang_thai = TrangThai.MIEU
        elif vi_tri_vu_khuc in [1, 3, 7, 9]:
            SaoVuKhuc.trang_thai = TrangThai.VUONG
        elif vi_tri_vu_khuc in [4, 10]:
            SaoVuKhuc.trang_thai = TrangThai.DAC
        elif vi_tri_vu_khuc in [6, 12]:
            SaoVuKhuc.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_vu_khuc


class SaoThienDong(Sao):
    name = 'Thiên Đồng'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_vu_khuc = SaoVuKhuc.an_sao(birthdate, cur_year)
        vi_tri_thien_dong = (vi_tri_vu_khuc - 2 + 12) % 12 + 1

        if vi_tri_thien_dong in [3, 9]:
            SaoThienDong.trang_thai = TrangThai.MIEU
        elif vi_tri_thien_dong in [1]:
            SaoThienDong.trang_thai = TrangThai.VUONG
        elif vi_tri_thien_dong in [4, 6, 12]:
            SaoThienDong.trang_thai = TrangThai.DAC
        elif vi_tri_thien_dong in [2, 5, 7, 8, 10, 11]:
            SaoThienDong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_dong


class SaoLiemTrinh(Sao):
    name = 'Liêm Trinh'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_dong = SaoThienDong.an_sao(birthdate, cur_year)
        vi_tri_liem_trinh = (vi_tri_thien_dong - 4 + 12) % 12 + 1

        if vi_tri_liem_trinh in [5, 11]:
            SaoLiemTrinh.trang_thai = TrangThai.MIEU
        elif vi_tri_liem_trinh in [1, 3, 7, 9]:
            SaoLiemTrinh.trang_thai = TrangThai.VUONG
        elif vi_tri_liem_trinh in [2, 8]:
            SaoLiemTrinh.trang_thai = TrangThai.DAC
        elif vi_tri_liem_trinh in [4, 6, 10, 12]:
            SaoLiemTrinh.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_liem_trinh


class SaoThienPhu(Sao):
    name = 'Thiên Phủ'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tu_vi = SaoTuVi.an_sao(birthdate, cur_year)
        temp_dict = {
            1: 5,
            2: 4,
            3: 3,
            4: 2,
            5: 1,
            6: 12,
            7: 11,
            8: 10,
            9: 9,
            10: 8,
            11: 7,
            12: 6,
        }

        vi_tri_thien_phu = temp_dict.get(vi_tri_tu_vi)
        if vi_tri_thien_phu in [1, 3, 7, 9]:
            SaoThienPhu.trang_thai = TrangThai.MIEU
        elif vi_tri_thien_phu in [5, 11]:
            SaoThienPhu.trang_thai = TrangThai.VUONG
        elif vi_tri_thien_phu in [6, 8, 12]:
            SaoThienPhu.trang_thai = TrangThai.DAC
        elif vi_tri_thien_phu in [2, 4, 10]:
            SaoThienPhu.trang_thai = TrangThai.BINH
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_phu


class SaoThaiAm(Sao):
    name = 'Thái Âm'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_phu = SaoThienPhu.an_sao(birthdate, cur_year)
        vi_tri_thai_am = vi_tri_thien_phu % 12 + 1

        if vi_tri_thai_am in [10, 11, 12]:
            SaoThaiAm.trang_thai = TrangThai.MIEU
        elif vi_tri_thai_am in [1, 9]:
            SaoThaiAm.trang_thai = TrangThai.VUONG
        elif vi_tri_thai_am in [2, 8]:
            SaoThaiAm.trang_thai = TrangThai.DAC
        elif vi_tri_thai_am in [3, 4, 5, 6, 7]:
            SaoThaiAm.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thai_am


class SaoThamLang(Sao):
    name = 'Tham Lang'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thai_am = SaoThaiAm.an_sao(birthdate, cur_year)
        vi_tri_tham_lang = vi_tri_thai_am % 12 + 1
        
        if vi_tri_tham_lang in [2, 8]:
            SaoThamLang.trang_thai = TrangThai.MIEU
        elif vi_tri_tham_lang in [5, 11]:
            SaoThamLang.trang_thai = TrangThai.VUONG
        elif vi_tri_tham_lang in [3, 9]:
            SaoThamLang.trang_thai = TrangThai.DAC
        elif vi_tri_tham_lang in [1, 4, 6, 7, 10, 12]:
            SaoThamLang.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_tham_lang


class SaoCuMon(Sao):
    name = 'Cự Môn'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tham_lang = SaoThamLang.an_sao(birthdate, cur_year)
        vi_tri_cu_mon = vi_tri_tham_lang % 12 + 1

        if vi_tri_cu_mon in [4, 10]:
            SaoCuMon.trang_thai = TrangThai.MIEU
        elif vi_tri_cu_mon in [1, 3, 7]:
            SaoCuMon.trang_thai = TrangThai.VUONG
        elif vi_tri_cu_mon in [9, 12]:
            SaoCuMon.trang_thai = TrangThai.DAC
        elif vi_tri_cu_mon in [2, 5, 6, 8, 11]:
            SaoCuMon.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_cu_mon


class SaoThienTuong(Sao):
    name = 'Thiên Tướng'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_cu_mon = SaoCuMon.an_sao(birthdate, cur_year)
        vi_tri_thien_tuong = vi_tri_cu_mon % 12 + 1

        if vi_tri_thien_tuong in [3, 9]:
            SaoThienTuong.trang_thai = TrangThai.MIEU
        elif vi_tri_thien_tuong in [1, 5, 7, 11]:
            SaoThienTuong.trang_thai = TrangThai.VUONG
        elif vi_tri_thien_tuong in [2, 6, 8, 12]:
            SaoThienTuong.trang_thai = TrangThai.DAC
        elif vi_tri_thien_tuong in [4, 10]:
            SaoThienTuong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_tuong


class SaoThienLuong(Sao):
    name = 'Thiên Lương'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_tuong = SaoThienTuong.an_sao(birthdate, cur_year)
        vi_tri_thien_luong = vi_tri_thien_tuong % 12 + 1

        if vi_tri_thien_luong in [5, 7, 11]:
            SaoThienLuong.trang_thai = TrangThai.MIEU
        elif vi_tri_thien_luong in [1, 3, 4, 9]:
            SaoThienLuong.trang_thai = TrangThai.VUONG
        elif vi_tri_thien_luong in [2, 8]:
            SaoThienLuong.trang_thai = TrangThai.DAC
        elif vi_tri_thien_luong in [6, 10, 12]:
            SaoThienLuong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_luong


class SaoThatSat(Sao):
    name = 'Thất Sát'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_luong = SaoThienLuong.an_sao(birthdate, cur_year)
        vi_tri_that_sat = vi_tri_thien_luong % 12 + 1

        if vi_tri_that_sat in [1, 3, 7, 9]:
            SaoThatSat.trang_thai = TrangThai.MIEU
        elif vi_tri_that_sat in [6, 12]:
            SaoThatSat.trang_thai = TrangThai.VUONG
        elif vi_tri_that_sat in [2, 8]:
            SaoThatSat.trang_thai = TrangThai.DAC
        elif vi_tri_that_sat in [4, 5, 10, 11]:
            SaoThatSat.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_that_sat


class SaoPhaQuan(Sao):
    name = 'Phá Quân'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.CHINH_TINH
    order = 2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_that_sat = SaoThatSat.an_sao(birthdate, cur_year)
        vi_tri_pha_quan = (vi_tri_that_sat + 3) % 12 + 1

        if vi_tri_pha_quan in [1, 7]:
            SaoPhaQuan.trang_thai = TrangThai.MIEU
        elif vi_tri_pha_quan in [2, 8]:
            SaoPhaQuan.trang_thai = TrangThai.VUONG
        elif vi_tri_pha_quan in [5, 11]:
            SaoPhaQuan.trang_thai = TrangThai.DAC
        elif vi_tri_pha_quan in [3, 4, 6, 9, 10, 12]:
            SaoPhaQuan.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_pha_quan


class SaoThienViet(Sao):
    name = 'Thiên Việt'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 4.5
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 8,
            2: 9,
            3: 10,
            4: 10,
            5: 8,
            6: 9,
            7: 3,
            8: 3,
            9: 6,
            10: 6
        }

        return temp_dict.get(can_nam)


class SaoHoaKhoa(Sao):
    name = 'Hoá Khoa'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 0.2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: SaoVuKhuc.an_sao(birthdate, cur_year, gender),
            2: SaoTuVi.an_sao(birthdate, cur_year, gender),
            3: SaoVanXuong.an_sao(birthdate, cur_year, gender),
            4: SaoThienCo.an_sao(birthdate, cur_year, gender),
            5: SaoHuuBat.an_sao(birthdate, cur_year, gender),
            6: SaoThienLuong.an_sao(birthdate, cur_year, gender),
            7: SaoThaiAm.an_sao(birthdate, cur_year, gender),
            8: SaoVanKhuc.an_sao(birthdate, cur_year, gender),
            9: SaoTaPhu.an_sao(birthdate, cur_year, gender),
            10: SaoThaiAm.an_sao(birthdate, cur_year, gender)
        }

        vi_tri_hoa_khoa = temp_dict.get(can_nam)
        if vi_tri_hoa_khoa in [3, 4, 5, 8, 11]:
            SaoHoaKhoa.trang_thai = TrangThai.VUONG
        elif vi_tri_hoa_khoa in [10]:
            SaoHoaKhoa.trang_thai = TrangThai.HAM
        elif vi_tri_hoa_khoa in [2, 6, 7, 9]:
            SaoHoaKhoa.trang_thai = TrangThai.DAC
        elif vi_tri_hoa_khoa in [1, 12]:
            SaoHoaKhoa.trang_thai = TrangThai.BINH
        else:
            raise InvalidViTri('Vi tri khong hop le.')

        return vi_tri_hoa_khoa


class SaoTaPhu(Sao):
    name = 'Tả Phù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 6
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_ta_phu = (4 + lunar_date.month - 1) % 12 + 1
        return vi_tri_ta_phu


class SaoPhiLiem(Sao):
    name = 'Phi Liêm'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 6 + 12) % 12 + 1


class SaoTrucPhu(Sao):
    name = 'Trực Phù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False

 
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_dieu_khach = SaoDieuKhach.an_sao(birthdate, cur_year, gender)
        return vi_tri_dieu_khach % 12 + 1


class SaoPhaToai(Sao):
    name = 'Phá Toái'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 6,
            2: 2,
            3: 10,
            4: 6,
            5: 2,
            6: 10,
            7: 6,
            8: 2,
            9: 10,
            10: 6,
            11: 2,
            12: 10
        }

        return temp_dict.get(chi_nam)


class SaoHiThan(Sao):
    name = 'Hỉ Thần'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 7 + 12) % 12 + 1


class SaoThienPhuc(Sao):
    name = 'Thiên Phúc'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 10,
            2: 9,
            3: 1,
            4: 12,
            5: 4,
            6: 3,
            7: 7,
            8: 6,
            9: 7,
            10: 6
        }

        return temp_dict.get(can_nam)


class SaoDiaKiep(Sao):
    name = 'Địa Kiếp'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 0
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_dia_kiep = (11 + zodiac_hour_tuple[1] - 1) % 12 + 1

        if vi_tri_dia_kiep in [3, 6, 9, 12]:
            SaoDiaKiep.trang_thai = TrangThai.DAC
        elif vi_tri_dia_kiep in [1, 2, 4, 5, 7, 8, 10, 11]:
            SaoDiaKiep.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_dia_kiep


class SaoThaiTue(Sao):
    name = 'Thái Tuế'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        return chi_nam


class SaoHoaLoc(Sao):
    name = 'Hoá Lộc'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 0
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: SaoLiemTrinh.an_sao(birthdate, cur_year, gender),
            2: SaoThienCo.an_sao(birthdate, cur_year, gender),
            3: SaoThienDong.an_sao(birthdate, cur_year, gender),
            4: SaoThaiAm.an_sao(birthdate, cur_year, gender),
            5: SaoThamLang.an_sao(birthdate, cur_year, gender),
            6: SaoVuKhuc.an_sao(birthdate, cur_year, gender),
            7: SaoThaiDuong.an_sao(birthdate, cur_year, gender),
            8: SaoCuMon.an_sao(birthdate, cur_year, gender),
            9: SaoThienLuong.an_sao(birthdate, cur_year, gender),
            10: SaoPhaQuan.an_sao(birthdate, cur_year, gender)
        }

        vi_tri_hoa_loc = temp_dict.get(can_nam)
        if vi_tri_hoa_loc in [3, 5, 11]:
            SaoHoaLoc.trang_thai = TrangThai.VUONG
        elif vi_tri_hoa_loc in [1, 7, 10, 12]:
            SaoHoaLoc.trang_thai = TrangThai.HAM
        elif vi_tri_hoa_loc in [2, 6, 9]:
            SaoHoaLoc.trang_thai = TrangThai.DAC
        elif vi_tri_hoa_loc in [4, 8]:
            SaoHoaLoc.trang_thai = TrangThai.BINH
        else:
            raise InvalidViTri('Vi tri khong hop le.')

        return vi_tri_hoa_loc


class SaoQuocAn(Sao):
    name = 'Quốc Ấn'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + 8) % 12 + 1


class SaoThieuDuong(Sao):
    name = 'Thiếu Dương'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thai_tue = SaoThaiTue.an_sao(birthdate, cur_year, gender)
        return vi_tri_thai_tue % 12 + 1


class SaoThienKhong(Sao):
    name = 'Thiên Không'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2.2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoThieuDuong.an_sao(birthdate, cur_year, gender)


class SaoBenhPhu(Sao):
    name = 'Bệnh Phù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 8 + 12) % 12 + 1


class SaoDiaGiai(Sao):
    name = 'Địa Giải'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 10
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_dia_giai = (7 + lunar_date.month - 1) % 12 + 1
        return vi_tri_dia_giai


class SaoThienMa(Sao):
    name = 'Thiên Mã'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 3,
            2: 12,
            3: 9,
            4: 6,
            5: 3,
            6: 12,
            7: 9,
            8: 6,
            9: 3,
            10: 12,
            11: 9,
            12: 6
        }

        vi_tri_thien_ma = temp_dict.get(chi_nam)
        if vi_tri_thien_ma in [3, 6]:
            SaoThienMa.trang_thai = TrangThai.DAC
        elif vi_tri_thien_ma in [9, 12]:
            SaoThienMa.trang_thai = TrangThai.HAM

        return vi_tri_thien_ma


class SaoHoaTinh(Sao):
    name = 'Hoả Tinh'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = -1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        zodiac_year_tuple = ZodiacUtil.zodiac_year_tuple(lunar_date)
        chi_nam = zodiac_year_tuple[1]
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)

        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        if chi_nam in [3, 7, 11]:
            vi_tri_hoa_tinh = (1 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        elif chi_nam in [1, 5, 9]:
            vi_tri_hoa_tinh = (2 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        elif chi_nam in [2, 6, 10]:
            vi_tri_hoa_tinh = (3 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        elif chi_nam in [4, 8, 12]:
            vi_tri_hoa_tinh = (9 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        if vi_tri_hoa_tinh in [3, 4, 5, 6, 7]:
            SaoHoaTinh.trang_thai = TrangThai.DAC
        elif vi_tri_hoa_tinh in [1, 2, 8, 9, 10, 11, 12]:
            SaoHoaTinh.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le. Sai trang thai.')
        
        return vi_tri_hoa_tinh


class SaoLinhTinh(Sao):
    name = 'Linh Tinh'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = -0.9
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        zodiac_year_tuple = ZodiacUtil.zodiac_year_tuple(lunar_date)
        chi_nam = zodiac_year_tuple[1]
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)

        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = -1
        else:
            d = 1

        if chi_nam in [3, 7, 11]:
            vi_tri_linh_tinh = (3 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        elif chi_nam in [1, 2, 4, 5, 6, 8, 9, 10, 12]:
            vi_tri_linh_tinh = (10 + d * (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        if vi_tri_linh_tinh in [3, 4, 5, 6, 7]:
            SaoLinhTinh.trang_thai = TrangThai.DAC
        elif vi_tri_linh_tinh in [1, 2, 8, 9, 10, 11, 12]:
            SaoLinhTinh.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le. Sai trang thai.')
        
        return vi_tri_linh_tinh


class SaoCoThan(Sao):
    name = 'Cô Thần'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 8.2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 3,
            2: 3,
            3: 6,
            4: 6,
            5: 6,
            6: 9,
            7: 9,
            8: 9,
            9: 12,
            10: 12,
            11: 12,
            12: 3
        }

        return temp_dict.get(chi_nam)


class SaoDaiHao(Sao):
    name = 'Đại Hao'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        vi_tri_dai_hao = (vi_tri_loc_ton - 1 + d * 9 + 12) % 12 + 1
        
        if vi_tri_dai_hao in [3, 4, 9, 10]:
            SaoDaiHao.trang_thai = TrangThai.DAC
        elif vi_tri_dai_hao in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoDaiHao.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_dai_hao


class SaoTangMon(Sao):
    name = 'Tang Môn'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thieu_duong = SaoThieuDuong.an_sao(birthdate, cur_year, gender)
        vi_tri_tang_mon = vi_tri_thieu_duong % 12 + 1

        if vi_tri_tang_mon in [3, 4, 9, 10]:
            SaoTangMon.trang_thai = TrangThai.DAC
        elif vi_tri_tang_mon in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoTangMon.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_tang_mon


class SaoThienQuy(Sao):
    name = 'Thiên Quý'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 1.05
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_van_khuc = SaoVanKhuc.an_sao(birthdate, cur_year, gender)
        vi_tri_thien_quy = (vi_tri_van_khuc - 1 - (lunar_date.day - 2) + 12 * 12) % 12 + 1
        return vi_tri_thien_quy


class SaoTauThu(Sao):
    name = 'Tấu Thư'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 5 + 12) % 12 + 1


class SaoDuongPhu(Sao):
    name = 'Đường Phù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + 5) % 12 + 1


class SaoThienTho(Sao):
    name = 'Thiên Thọ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 26
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        vi_tri_cung_than = TuViUtil.tim_vi_tri_than(birthdate)
        return (vi_tri_cung_than - 1 + (chi_nam - 1) + 12) % 12 + 1


class SaoGiaiThan(Sao):
    name = 'Giải Thần'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoPhuongCac.an_sao(birthdate, cur_year, gender)
    

class SaoPhuongCac(Sao):
    name = 'Phượng Các'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        return (10 - (chi_nam - 1) + 12) % 12 + 1


class SaoDiaKhong(Sao):
    name = 'Địa Không'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = -0.1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_dia_khong = (11 - (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1

        if vi_tri_dia_khong in [3, 6, 9, 12]:
            SaoDiaKhong.trang_thai = TrangThai.DAC
        elif vi_tri_dia_khong in [1, 2, 4, 5, 7, 8, 10, 11]:
            SaoDiaKhong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_dia_khong


class SaoQuaTu(Sao):
    name = 'Quả Tú'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 8.2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 11,
            2: 11,
            3: 2,
            4: 2,
            5: 2,
            6: 5,
            7: 5,
            8: 5,
            9: 8,
            10: 8,
            11: 8,
            12: 11
        }

        return temp_dict.get(chi_nam)


class SaoDieuKhach(Sao):
    name = 'Điếu Khách'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_phuc_duc = SaoPhucDuc.an_sao(birthdate, cur_year, gender)
        return vi_tri_phuc_duc % 12 + 1


class SaoThienLa(Sao):
    name = 'Thiên La'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 1000
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return 5


class SaoHuuBat(Sao):
    name = 'Hữu Bật'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 6.1
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_huu_bat = (10 - (lunar_date.month - 1) + 12) % 12 + 1
        return vi_tri_huu_bat


class SaoHongLoan(Sao):
    name = 'Hồng Loan'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 12.1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        return (3 - (chi_nam - 1) + 12) % 12 + 1


class SaoThienGiai(Sao):
    name = 'Thiên Giải'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 10
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_thien_giai = (8 + lunar_date.month - 1) % 12 + 1
        return vi_tri_thien_giai


class SaoPhongCao(Sao):
    name = 'Phong Cáo'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 11
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_phong_cao = (2 + zodiac_hour_tuple[1] - 1) % 12 + 1
        return vi_tri_phong_cao


class SaoThienTru(Sao):
    name = 'Thiên Trù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 6,
            2: 7,
            3: 1,
            4: 6,
            5: 7,
            6: 9,
            7: 3,
            8: 7,
            9: 10,
            10: 11
        }

        return temp_dict.get(can_nam)


class SaoThieuAm(Sao):
    name = 'Thiếu Âm'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 25
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tang_mon = SaoTangMon.an_sao(birthdate, cur_year, gender)
        return vi_tri_tang_mon % 12 + 1


class SaoPhucBinh(Sao):
    name = 'Phục Binh'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 10 + 12) % 12 + 1


class SaoVanXuong(Sao):
    name = 'Văn Xương'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 1.2
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_van_xuong = (10 - (zodiac_hour_tuple[1] - 1) + 12) % 12 + 1
        
        if vi_tri_van_xuong in [1, 3, 7, 9]:
            SaoVanXuong.trang_thai = TrangThai.HAM
        elif vi_tri_van_xuong in [2, 4, 5, 6, 8, 10, 11, 12]:
            SaoVanXuong.trang_thai = TrangThai.DAC
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_van_xuong


class SaoThienKhoi(Sao):
    name = 'Thiên Khôi'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 4.5
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 2,
            2: 1,
            3: 12,
            4: 12,
            5: 2,
            6: 1,
            7: 7,
            8: 7,
            9: 4,
            10: 4
        }

        return temp_dict.get(can_nam)


class SaoThienHy(Sao):
    name = 'Thiên Hỷ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 11.9
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        return (9 - (chi_nam - 1) + 12) % 12 + 1


class SaoDaoHoa(Sao):
    name = 'Đào Hoa'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 12
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 10,
            2: 7,
            3: 4,
            4: 1,
            5: 10,
            6: 7,
            7: 4,
            8: 1,
            9: 10,
            10: 7,
            11: 4,
            12: 1
        }

        return temp_dict.get(chi_nam)


class SaoPhucDuc(Sao):
    name = 'Phúc Đức'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 25
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_bach_ho = SaoBachHo.an_sao(birthdate, cur_year, gender)
        return vi_tri_bach_ho % 12 + 1


class SaoThienDuc(Sao):
    name = 'Thiên Đức'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoPhucDuc.an_sao(birthdate, cur_year, gender)


class SaoTuongQuan(Sao):
    name = 'Tướng Quân'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 5.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 4 + 12) % 12 + 1


class SaoThienSu(Sao):
    name = 'Thiên Sứ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 1000
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return TuViUtil.tim_cung_tat_ach(birthdate)


class SaoAnQuang(Sao):
    name = 'Ân Quang'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 1.04
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_van_xuong = SaoVanXuong.an_sao(birthdate, cur_year, gender)
        vi_tri_an_quang = (vi_tri_van_xuong - 1 + (lunar_date.day - 2) + 12 * 12) % 12 + 1
        return vi_tri_an_quang


class SaoThienQuan(Sao):
    name = 'Thiên Quan'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 8,
            2: 5,
            3: 6,
            4: 3,
            5: 4,
            6: 10,
            7: 12,
            8: 10,
            9: 11,
            10: 7
        }

        return temp_dict.get(can_nam)


class SaoHoaCai(Sao):
    name = 'Hoa Cái'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 12
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 5,
            2: 2,
            3: 11,
            4: 8,
            5: 5,
            6: 2,
            7: 11,
            8: 8,
            9: 5,
            10: 2,
            11: 11,
            12: 8
        }

        return temp_dict.get(chi_nam)


class SaoLongTri(Sao):
    name = 'Long Trì'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoQuanPhuf.an_sao(birthdate, cur_year, gender)


class SaoDaLa(Sao):
    name = 'Đà La'
    am_duong = AmDuong.AM
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 0
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        vi_tri_da_la = (vi_tri_loc_ton - 2 + 12) % 12 + 1

        if vi_tri_da_la in [2, 5, 8, 11]:
            SaoDaLa.trang_thai = TrangThai.DAC
        elif vi_tri_da_la in [1, 3, 4, 6, 7, 9, 10, 12]:
            SaoDaLa.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_da_la


class SaoHoaKy(Sao):
    name = 'Hoá Kỵ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 0.8
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: SaoThaiDuong.an_sao(birthdate, cur_year, gender),
            2: SaoThaiAm.an_sao(birthdate, cur_year, gender),
            3: SaoLiemTrinh.an_sao(birthdate, cur_year, gender),
            4: SaoCuMon.an_sao(birthdate, cur_year, gender),
            5: SaoThienCo.an_sao(birthdate, cur_year, gender),
            6: SaoVanKhuc.an_sao(birthdate, cur_year, gender),
            7: SaoThienDong.an_sao(birthdate, cur_year, gender),
            8: SaoVanXuong.an_sao(birthdate, cur_year, gender),
            9: SaoVuKhuc.an_sao(birthdate, cur_year, gender),
            10: SaoThamLang.an_sao(birthdate, cur_year, gender)
        }

        vi_tri_hoa_ky = temp_dict.get(can_nam)
        if vi_tri_hoa_ky in [2, 5, 8, 11]:
            SaoHoaKy.trang_thai = TrangThai.DAC
        elif vi_tri_hoa_ky in [1, 3, 4, 6, 7, 9, 10, 12]:
            SaoHoaKy.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')

        return vi_tri_hoa_ky


class SaoThienHinh(Sao):
    name = 'Thiên Hình'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 3
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_thien_hinh = (9 + lunar_date.month - 1) % 12 + 1

        if vi_tri_thien_hinh in [3, 4, 9, 10]:
            SaoThienHinh.trang_thai = TrangThai.DAC
        elif vi_tri_thien_hinh in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoThienHinh.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_hinh


class SaoQuanPhur(Sao):
    name = 'Quan Phủ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 11 + 12) % 12 + 1


class SaoQuanPhuf(Sao):
    name = 'Quan Phù'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thieu_am = SaoThieuAm.an_sao(birthdate, cur_year, gender)
        return vi_tri_thieu_am % 12 + 1


class SaoDiaVong(Sao):
    name = 'Địa Võng'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 1000
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return 11


class SaoHoaQuyen(Sao):
    name = 'Hoá Quyền'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 0.1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: SaoPhaQuan.an_sao(birthdate, cur_year, gender),
            2: SaoThienLuong.an_sao(birthdate, cur_year, gender),
            3: SaoThienCo.an_sao(birthdate, cur_year, gender),
            4: SaoThienDong.an_sao(birthdate, cur_year, gender),
            5: SaoThaiAm.an_sao(birthdate, cur_year, gender),
            6: SaoThamLang.an_sao(birthdate, cur_year, gender),
            7: SaoVuKhuc.an_sao(birthdate, cur_year, gender),
            8: SaoThaiDuong.an_sao(birthdate, cur_year, gender),
            9: SaoTuVi.an_sao(birthdate, cur_year, gender),
            10: SaoCuMon.an_sao(birthdate, cur_year, gender)
        }

        vi_tri_hoa_quyen = temp_dict.get(can_nam)
        if vi_tri_hoa_quyen in [3, 4, 8, 11]:
            SaoHoaQuyen.trang_thai = TrangThai.VUONG
        elif vi_tri_hoa_quyen in [1, 9, 10]:
            SaoHoaQuyen.trang_thai = TrangThai.HAM
        elif vi_tri_hoa_quyen in [2]:
            SaoHoaQuyen.trang_thai = TrangThai.DAC
        elif vi_tri_hoa_quyen in [5, 6, 7, 12]:
            SaoHoaQuyen.trang_thai = TrangThai.BINH
        else:
            raise InvalidViTri('Vi tri khong hop le.')

        return vi_tri_hoa_quyen


class SaoThienY(Sao):
    name = 'Thiên Y'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = -1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_thien_y = (1 + lunar_date.month - 1) % 12 + 1

        if vi_tri_thien_y in [3, 4, 9, 10]:
            SaoThienY.trang_thai = TrangThai.DAC
        elif vi_tri_thien_y in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoThienY.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_y


class SaoLNVanTinh(Sao):
    name = 'LN Văn Tinh'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + 3) % 12 + 1


class SaoThienTai(Sao):
    name = 'Thiên Tài'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        vi_tri_cung_menh = TuViUtil.tim_vi_tri_menh(birthdate)
        return (vi_tri_cung_menh - 1 - (chi_nam - 1) + 12) % 12 + 1


class SaoThienDieu(Sao):
    name = 'Thiên Diêu'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = -0.9
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_dieu = SaoThienY.an_sao(birthdate, cur_year)
        SaoThienDieu.trang_thai = SaoThienY.trang_thai
        return vi_tri_thien_dieu


class SaoTieuHao(Sao):
    name = 'Tiểu Hao'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 15.1
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        vi_tri_tieu_hao = (vi_tri_loc_ton - 1 + d * 3 + 12) % 12 + 1

        if vi_tri_tieu_hao in [3, 4, 9, 10]:
            SaoTieuHao.trang_thai = TrangThai.DAC
        elif vi_tri_tieu_hao in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoTieuHao.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_tieu_hao


class SaoBachHo(Sao):
    name = 'Bạch Hổ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_long_duc = SaoLongDuc.an_sao(birthdate, cur_year, gender)
        vi_tri_bach_ho = vi_tri_long_duc % 12 + 1

        if vi_tri_bach_ho in [3, 4, 9, 10]:
            SaoBachHo.trang_thai = TrangThai.DAC
        elif vi_tri_bach_ho in [1, 2, 5, 6, 7, 8, 11, 12]:
            SaoBachHo.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_bach_ho


class SaoThaiPhu(Sao):
    name = 'Thai Phụ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 0.9
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_thai_phu = (6 + zodiac_hour_tuple[1] - 1) % 12 + 1
        return vi_tri_thai_phu


class SaoTamThai(Sao):
    name = 'Tam Thai'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 3.5
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_ta_phu = SaoTaPhu.an_sao(birthdate, cur_year, gender)
        vi_tri_tam_thai = (vi_tri_ta_phu - 1 + lunar_date.day - 1) % 12 + 1
        return vi_tri_tam_thai


class SaoBatToa(Sao):
    name = 'Bát Toạ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 3.6
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        vi_tri_huu_bat = SaoHuuBat.an_sao(birthdate, cur_year, gender)
        vi_tri_bat_toa = (vi_tri_huu_bat - 1 - (lunar_date.day - 1) + 12 * 12) % 12 + 1
        return vi_tri_bat_toa


class SaoThanhLong(Sao):
    name = 'Thanh Long'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 2 + 12) % 12 + 1


class SaoLongDuc(Sao):
    name = 'Long Đức'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tue_pha = SaoTuePha.an_sao(birthdate, cur_year, gender)
        return vi_tri_tue_pha % 12 + 1


class SaoThienThuong(Sao):
    name = 'Thiên Thương'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 1000
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return TuViUtil.tim_cung_no_boc(birthdate)


class SaoLucSi(Sao):
    name = 'Lực Sĩ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_loc_ton - 1 + d * 1 + 12) % 12 + 1


class SaoKinhDuong(Sao):
    name = 'Kình Dương'
    am_duong = AmDuong.DUONG
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 0
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_loc_ton = SaoLocTon.an_sao(birthdate, cur_year, gender)
        vi_tri_kinh_duong = vi_tri_loc_ton % 12 + 1

        if vi_tri_kinh_duong in [2, 5, 8, 11]:
            SaoKinhDuong.trang_thai = TrangThai.DAC
        elif vi_tri_kinh_duong in [1, 3, 4, 6, 7, 9, 10, 12]:
            SaoKinhDuong.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_kinh_duong


class SaoTuePha(Sao):
    name = 'Tuế Phá'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_tu_phu = SaoTuPhu.an_sao(birthdate, cur_year, gender)
        return vi_tri_tu_phu % 12 + 1


class SaoThienHu(Sao):
    name = 'Thiên Hư'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 8
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_thien_hu = SaoTuePha.an_sao(birthdate, cur_year, gender)
        if vi_tri_thien_hu in [1, 3, 7, 9]:
            SaoThienHu.trang_thai = TrangThai.DAC
        elif vi_tri_thien_hu in [2, 4, 5, 6, 8, 10, 11, 12]:
            SaoThienHu.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_hu


class SaoThienKhoc(Sao):
    name = 'Thiên Khốc'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 8.1
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        vi_tri_thien_khoc = (6 - (chi_nam - 1) + 12) % 12 + 1

        if vi_tri_thien_khoc in [1, 3, 7, 9]:
            SaoThienKhoc.trang_thai = TrangThai.DAC
        elif vi_tri_thien_khoc in [2, 4, 5, 6, 8, 10, 11, 12]:
            SaoThienKhoc.trang_thai = TrangThai.HAM
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_thien_khoc


class SauDauQuan(Sao):
    name = 'Đẩu Quân'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 31
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        chi_gio = ZodiacUtil.zodiac_hour_tuple(birthdate)[1]
        return (chi_nam - 1 - (lunar_date.month - 1) + (chi_gio - 1) + 12) % 12 + 1


class SaoVanKhuc(Sao):
    name = 'Văn Khúc'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 1.1
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        zodiac_hour_tuple = ZodiacUtil.zodiac_hour_tuple(birthdate)
        vi_tri_van_khuc = (4 + zodiac_hour_tuple[1] - 1) % 12 + 1
        
        if vi_tri_van_khuc in [1, 3, 7, 9]:
            SaoVanKhuc.trang_thai = TrangThai.HAM 
        elif vi_tri_van_khuc in [2, 4, 5, 6, 8, 10, 11, 12]:
            SaoVanKhuc.trang_thai = TrangThai.DAC
        else:
            raise InvalidViTri('Vi tri khong hop le.')
        
        return vi_tri_van_khuc


class SaoLocTon(Sao):
    name = 'Lộc Tồn'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = -0.8
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 3,
            2: 4,
            3: 6,
            4: 7,
            5: 6,
            6: 7,
            7: 9,
            8: 10,
            9: 12,
            10: 1
        }

        vi_tri_loc_ton = temp_dict.get(can_nam)
        if vi_tri_loc_ton in [1, 3, 4, 7]:
            SaoLocTon.trang_thai = TrangThai.MIEU
        elif vi_tri_loc_ton in [6, 12]:
            SaoLocTon.trang_thai = TrangThai.DAC
        elif vi_tri_loc_ton in [9, 10]:
            SaoLocTon.trang_thai = TrangThai.BINH
        else:
            raise InvalidViTri('Vi tri khong hop le')

        return vi_tri_loc_ton


class SaoBacSy(Sao):
    name = 'Bác Sỹ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 15
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoLocTon.an_sao(birthdate, cur_year, gender)


class SaoNguyetDuc(Sao):
    name = 'Nguyệt Đức'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        return SaoTuPhu.an_sao(birthdate, cur_year, gender)


class SaoLuuHa(Sao):
    name = 'Lưu Hà'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 4.5
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 10,
            2: 11,
            3: 8,
            4: 9,
            5: 6,
            6: 7,
            7: 4,
            8: 5,
            9: 12,
            10: 3
        }

        return temp_dict.get(can_nam)


class SaoTuPhu(Sao):
    name = 'Tử Phủ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 25
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_quan_phuf = SaoQuanPhuf.an_sao(birthdate, cur_year, gender)
        return vi_tri_quan_phuf % 12 + 1


class SaoKiepSat(Sao):
    name = 'Kiếp Sát'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 30
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]

        temp_dict = {
            1: 6,
            2: 3,
            3: 12,
            4: 9,
            5: 6,
            6: 3,
            7: 12,
            8: 9,
            9: 6,
            10: 3,
            11: 12,
            12: 9
        }

        return temp_dict.get(chi_nam)


class SaoTruongSinh(Sao):
    name = 'Trường Sinh'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        cuc = TuViUtil.tim_cuc(birthdate)
        temp_dict = {
            'Thuỷ nhị cục': 9,
            'Mộc tam cục': 12,
            'Kim tứ cục': 6,
            'Thổ ngũ cục': 9,
            'Hoả lục cục': 3,
        }

        return temp_dict.get(cuc)


class SaoMocDuc(Sao):
    name = 'Mộc Dục'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoTruongSinh.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoQuanDoi(Sao):
    name = 'Quan Đới'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoMocDuc.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoLamQuan(Sao):
    name = 'Lâm Quan'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoQuanDoi.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoDeVuong(Sao):
    name = 'Đế Vượng'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoLamQuan.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoSuy(Sao):
    name = 'Suy'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoDeVuong.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoBenh(Sao):
    name = 'Bệnh'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoSuy.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoTu(Sao):
    name = 'Tử'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoBenh.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoMo(Sao):
    name = 'Mộ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoTu.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoTuyet(Sao):
    name = 'Tuyệt'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoMo.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoThai(Sao):
    name = 'Thai'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoTuyet.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1


class SaoDuong(Sao):
    name = 'Dưỡng'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_DUOI
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        am_duong = TuViUtil.tim_am_duong(birthdate, gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        return (SaoThai.an_sao(birthdate, cur_year, gender) - 1 + d + 12) % 12 + 1
    

class SaoTuan(Sao):
    name = 'Tuần'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.NONE
    order = None
    is_print_bold = True

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam, chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)
        vi_tri_tuan_sau_2_cung = (chi_nam - 1 - (can_nam - 1) + 12) % 12 + 1
        vi_tri_tuan = (vi_tri_tuan_sau_2_cung - 3 + 12) % 12 + 1
        return vi_tri_tuan


class SaoTriet(Sao):
    name = 'Triệt'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.NONE
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.NONE
    order = None
    is_print_bold = True


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]

        temp_dict = {
            1: 9,
            2: 7,
            3: 5,
            4: 3,
            5: 1,
            6: 9,
            7: 7,
            8: 5,
            9: 3,
            10: 1
        }

        return temp_dict.get(can_nam)


class SaoLuuThienMa(Sao):
    name = 'L. Thiên Mã'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 2000
    is_print_bold = False

    
    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        temp_dict = {
            1: 3,
            2: 12,
            3: 9,
            4: 6,
            5: 3,
            6: 12,
            7: 9,
            8: 6,
            9: 3,
            10: 12,
            11: 9,
            12: 6
        }

        return temp_dict.get(chi_nam_xem)


class SaoLuuTangMon(Sao):
    name = 'L. Tang Môn'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.MOC
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2000
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        return (2 + (chi_nam_xem - 1)) % 12 + 1


class SaoLuuThienHu(Sao):
    name = 'L. Thiên Hư'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THUY
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2001
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        return (6 + (chi_nam_xem - 1)) % 12 + 1


class SaoLuuThaiTue(Sao):
    name = 'L. Thái Tuế'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.HOA
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2002
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        return chi_nam_xem


class SaoLuuThienKhoc(Sao):
    name = 'L. Thiên Khốc'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2003
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        return (6 - (chi_nam_xem - 1) + 12) % 12 + 1


class SaoLuuKinhDuong(Sao):
    name = 'L. Kình Dương'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2010
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_luu_loc_ton = SaoLuuLocTon.an_sao(birthdate, cur_year, gender)
        return vi_tri_luu_loc_ton % 12 + 1


class SaoLuuLocTon(Sao):
    name = 'L. Lộc Tồn'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.THO
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_TRAI
    order = 2001
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        can_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[0]
        temp_dict = {
            1: 3,
            2: 4,
            3: 6,
            4: 7,
            5: 6,
            6: 7,
            7: 9,
            8: 10,
            9: 12,
            10: 1,
        }
        
        return temp_dict.get(can_nam_xem)


class SaoLuuBachHo(Sao):
    name = 'L. Bạch Hổ'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2004
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(cur_year, 6, 1))[1]
        return (8 + (chi_nam_xem - 1)) % 12 + 1


class SaoLuuDaLa(Sao):
    name = 'L. Đà La'
    am_duong = AmDuong.NONE
    ngu_hanh = NguHanh.KIM
    trang_thai = TrangThai.NONE
    loai_sao = LoaiSao.PHU_TINH_PHAI
    order = 2015
    is_print_bold = False


    @staticmethod
    @lru_cache
    def an_sao(birthdate: SolarDate, cur_year: int = 2023, gender: Union[int, None] = GioiTinh.NONE.value) -> int:
        vi_tri_luu_loc_ton = SaoLuuLocTon.an_sao(birthdate, cur_year, gender)
        return (vi_tri_luu_loc_ton - 2 + 12) % 12 + 1
    