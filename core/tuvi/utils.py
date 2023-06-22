from core.tuvi.elements.gioitinh import GioiTinh
from core.tuvi.elements.amduong import AmDuong
from core.tuvi.elements.nguhanh import NguHanh
from core.tuvi.elements.chi import Chi
from core.utils import NguHanhUtil, ZodiacUtil, DateUtil
from core.date import Date, LunarDate, SolarDate
from core.exceptions import InvalidChi, InvalidGioiTinh, InvalidViTriThan


class TuViUtil:
    @staticmethod
    def tim_am_duong(birthdate: SolarDate, gender: int) -> str:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        zodiac_year_tuple = ZodiacUtil.zodiac_year_tuple(lunar_date)

        if zodiac_year_tuple[0] % 2 == 1:
            if gender == GioiTinh.NAM.value:
                return 'Dương Nam'
            elif gender == GioiTinh.NU.value:
                return 'Dương Nữ'
            else:
                raise InvalidGioiTinh('Invalid gender.')
        else:
            if gender == GioiTinh.NAM.value:
                return 'Âm Nam'
            elif gender == GioiTinh.NU.value:
                return 'Âm Nữ'
            else:
                raise InvalidGioiTinh('Invalid gender.')


    @staticmethod
    def tim_menh(birthdate: SolarDate) -> str:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        temp_dict = {
            "K1": "Hải Trung Kim",
            "T1": "Giản Hạ Thuỷ",
            "H1": "Tích Lịch Hoả",
            "O1": "Bích Thượng Thổ",
            "M1": "Tang Đố Mộc",
            "T2": "Đại Khê Thuỷ",
            "H2": "Lư Trung Hoả",
            "O2": "Thành Đầu Thổ",
            "M2": "Tùng Bách Mộc",
            "K2": "Kim Bạch Kim",
            "H3": "Phúc Đăng Hoả",
            "O3": "Sa Trung Thổ",
            "M3": "Đại Lâm Mộc",
            "K3": "Bạch Lạp Kim",
            "T3": "Trường Lưu Thuỷ",
            "K4": "Sa Trung Kim",
            "T4": "Thiên Hà Thuỷ",
            "H4": "Thiên Thượng Hoả",
            "O4": "Lộ Bàng Thổ",
            "M4": "Dương Liễu Mộc",
            "T5": "Tuyền Trung Thuỷ",
            "H5": "Sơn Hạ Hoả",
            "O5": "Đại Trạch Thổ",
            "M5": "Thạch Lựu Mộc",
            "K5": "Kiếm Phong Kim",
            "H6": "Sơn Đầu Hoả",
            "O6": "Ốc Thượng Thổ",
            "M6": "Bình Địa Mộc",
            "K6": "Thoa Xuyến Kim",
            "T6": "Đại Hải Thuỷ"
        }

        matrix = [
            [0, "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"],
            [1, "K1", False, "T1", False, "H1", False, "O1", False, "M1", False],
            [2, False, "K1", False, "T1", False, "H1", False, "O1", False, "M1"],
            [3, "T2", False, "H2", False, "O2", False, "M2", False, "K2", False],
            [4, False, "T2", False, "H2", False, "O2", False, "M2", False, "K2"],
            [5, "H3", False, "O3", False, "M3", False, "K3", False, "T3", False],
            [6, False, "H3", False, "O3", False, "M3", False, "K3", False, "T3"],
            [7, "K4", False, "T4", False, "H4", False, "O4", False, "M4", False],
            [8, False, "K4", False, "T4", False, "H4", False, "O4", False, "M4"],
            [9, "T5", False, "H5", False, "O5", False, "M5", False, "K5", False],
            [10, False, "T5", False, "H5", False, "O5", False, "M5", False, "K5"],
            [11, "H6", False, "O6", False, "M6", False, "K6", False, "T6", False],
            [12, False, "H6", False, "O6", False, "M6", False, "K6", False, "T6"]
        ]
        

        can, chi = ZodiacUtil.zodiac_year_tuple(lunar_date)
        return temp_dict.get(matrix[chi][can])


    @staticmethod
    def tim_cuc(birthdate: SolarDate) -> str:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        can_nam_index = (ZodiacUtil.zodiac_year_tuple(lunar_date)[0] - 1) % 5 + 1
        vi_tri_menh = TuViUtil.tim_vi_tri_menh(birthdate)
        
        if vi_tri_menh in [Chi.TI.value, Chi.SUU.value]:
            menh_index = 1
        elif vi_tri_menh in [Chi.DAN.value, Chi.MAO.value, Chi.TUAT.value, Chi.HOI.value]:
            menh_index = 2
        elif vi_tri_menh in [Chi.NGO.value, Chi.MUI.value]:
            menh_index = 3
        elif vi_tri_menh in [Chi.TY.value, Chi.THIN.value]:
            menh_index = 4
        elif vi_tri_menh in [Chi.THAN.value, Chi.DAU.value]:
            menh_index = 5
        else:
            raise InvalidChi('Invalid zodiac[1].')
        

        final_index = (can_nam_index + menh_index - 1) % 5 + 1
        temp_dict = {
            1: 'Kim tứ cục',
            2: 'Thuỷ nhị cục',
            3: 'Hoả lục cục',
            4: 'Thổ ngũ cục',
            5: 'Mộc tam cục',
        }

        return temp_dict.get(final_index)


    @staticmethod
    def tim_chu_menh(birthdate: SolarDate) -> str:
        vi_tri_menh = TuViUtil.tim_vi_tri_menh(birthdate)

        temp_dict = {
            1: 'Tham Lang',
            2: 'Cự Môn',
            3: 'Lộc Tồn',
            4: 'Văn Khúc',
            5: 'Liêm Trinh',
            6: 'Vũ Khúc',
            7: 'Phá Quân',
            8: 'Vũ Khúc',
            9: 'Liêm Trinh', 
            10: 'Văn Khúc',
            11: 'Lộc Tồn',
            12: 'Cự Môn',
        }

        return temp_dict.get(vi_tri_menh)


    @staticmethod
    def tim_chu_than(birthdate: SolarDate) -> str:
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        temp_dict = {
            1: 'Linh Tinh',
            2: 'Thiên Tướng',
            3: 'Thiên Lương',
            4: 'Thiên Đồng',
            5: 'Văn Xương',
            6: 'Thiên Cơ',
            7: 'Hoả Tinh',
            8: 'Thiên Tướng',
            9: 'Thiên Lương',
            10: 'Thiên Đồng',
            11: 'Văn Xương',
            12: 'Thiên Cơ',
        }

        return temp_dict.get(chi_nam)


    @staticmethod
    def tim_vi_tri_menh(birthdate: SolarDate) -> int:
        """
        NOTE: This `birthdate` must be a solar date.
        """

        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        month = lunar_date.month
        hour = ZodiacUtil.zodiac_hour_tuple(birthdate)[1]
        return (2 + (month - 1) - (hour - 1) + 12) % 12 + 1


    @staticmethod
    def tim_vi_tri_than(birthdate: SolarDate) -> int:
        """
        NOTE: This `birthdate` must be a solar date.
        """

        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        month = lunar_date.month
        hour = ZodiacUtil.zodiac_hour_tuple(birthdate)[1]
        return (2 + (month - 1) + (hour - 1)) % 12 + 1


    @staticmethod
    def tim_tinh_ly_am_duong(birthdate: SolarDate) -> str:
        """
        NOTE: This `birthdate` must be a solar date.
        """

        vi_tri_menh = TuViUtil.tim_vi_tri_menh(birthdate)
        lunar_date = DateUtil.solar_to_lunar(birthdate.empty_hms())
        zodiac_year_tuple = ZodiacUtil.zodiac_year_tuple(lunar_date)
     
        if (zodiac_year_tuple[0] % 2 == 1 and vi_tri_menh % 2 == 1) or (zodiac_year_tuple[0] % 2 == 0 and vi_tri_menh % 2 == 0):
            return 'Âm Dương thuận lý'
        else:
            return 'Âm Dương nghịch lý'


    @staticmethod
    def tim_cuc_menh_sinh_khac(birthdate: SolarDate) -> str:
        menh = TuViUtil.tim_menh(birthdate).split()[-1]
        cuc = TuViUtil.tim_cuc(birthdate).split()[0]
        ngu_hanh_menh = NguHanhUtil.ngu_hanh_from_string(menh)
        ngu_hanh_cuc = NguHanhUtil.ngu_hanh_from_string(cuc)

        if NguHanhUtil.check_tuong_sinh(ngu_hanh_menh, ngu_hanh_cuc):
            if ngu_hanh_menh == NguHanhUtil.get_ngu_hanh_sinh_cho(ngu_hanh_cuc):
                return 'Mệnh sinh Cục'
            else:
                return 'Cục sinh Mệnh'

        elif NguHanhUtil.check_tuong_khac(ngu_hanh_menh, ngu_hanh_cuc):
            if ngu_hanh_menh == NguHanhUtil.get_ngu_hanh_khac_che(ngu_hanh_cuc):
                return 'Mệnh khắc Cục'
            else:
                return 'Cục khắc Mệnh'
        else:
            return 'Mệnh Cục bình hoà'


    @staticmethod
    def tim_noi_cu_than(birthdate: SolarDate, gender: int) -> str:
        """
        NOTE: This `birthdate` must be a solar date.
        """

        if gender not in [GioiTinh.NAM.value, GioiTinh.NU.value]:
            raise InvalidGioiTinh('Invalid gender.')

        vi_tri_menh = TuViUtil.tim_vi_tri_menh(birthdate)
        vi_tri_than = TuViUtil.tim_vi_tri_than(birthdate)
        distance = (vi_tri_than - vi_tri_menh + 12) % 12

        if distance % 2 == 1:
            raise InvalidViTriThan('Vi tri than khong hop le.')
        
        temp_dict = {
            0: 'Thân Mệnh đồng cung',
            2: 'Thân cư Phúc Đức',
            4: 'Thân cư Quan Lộc',
            6: 'Thân cư Thiên Di',
            8: 'Thân cư Tài Bạch',
            10: 'Thân cư ' + ('Thê' if gender == GioiTinh.NAM.value else 'Phu'),
        }

        return temp_dict.get(distance)
    

    @staticmethod
    def tim_cung_phu_mau(birthdate: SolarDate) -> int:
        return TuViUtil.tim_vi_tri_menh(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_phuc_duc(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_phu_mau(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_dien_trach(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_phuc_duc(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_quan_loc(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_dien_trach(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_no_boc(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_quan_loc(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_thien_di(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_no_boc(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_tat_ach(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_thien_di(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_tai_bach(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_tat_ach(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_tu_tuc(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_tai_bach(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_phu_the(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_tu_tuc(birthdate) % 12 + 1
    

    @staticmethod
    def tim_cung_huynh_de(birthdate: SolarDate) -> int:
        return TuViUtil.tim_cung_phu_the(birthdate) % 12 + 1
