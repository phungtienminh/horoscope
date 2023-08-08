from core.tuvi.structures.odiaban import ODiaBan
from core.date import Date, SolarDate
from core.tuvi.elements.gioitinh import GioiTinh
from core.tuvi.elements.can import Can
from core.tuvi.elements.chi import Chi
from core.tuvi.elements.trangthai import TrangThai
from core.tuvi.stars.sao import SaoRegistry
from core.tuvi.utils import TuViUtil
from core.utils import ZodiacUtil, DateUtil
from core.exceptions import InvalidGioiTinh, InvalidViTri
from core.localizer import VNLocalizer
from core.draw import Color, FontSize, get_position, get_color, get_color_by_nguhanh

from typing import Union, List

from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime, timedelta


class LaSoTuVi:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int = 0, gender: Union[int, None] = GioiTinh.NONE.value, cur_year: int = 2023, hoten: str = 'Tử vi Tiến Minh') -> None:
        self.old_year = year
        self.old_month = month
        self.old_day = day
        self.old_hour = hour
        self.old_minute = minute

        if hour >= 23:
            current_date = datetime(year, month, day)
            next_date = current_date + timedelta(days=1)

            year = next_date.year
            month = next_date.month
            day = next_date.day
            hour = 0
            minute = 0


        self.birthdate: SolarDate = SolarDate(year, month, day, hour, minute, second)
        self.gender: int = gender
        self.cur_year: int = cur_year
        self.hoten = hoten

        self.diaban: List[ODiaBan] = [ODiaBan(i + 1) for i in range(12)]
        self.vi_tri_tuan: Union[int, None] = None
        self.vi_tri_triet: Union[int, None] = None

        # Prepare state
        self._prepare()


    def _prepare(self) -> None:
        """
        Prepare all positions of stars. 
        NOTE: This is a private method, should not be called outside this class scope.
        """
        for sao in SaoRegistry.get_subclasses():
            vi_tri = sao.an_sao(self.birthdate, self.cur_year, self.gender)
            if sao.name == 'Tuần':
                self.vi_tri_tuan = vi_tri
            elif sao.name == 'Triệt':
                self.vi_tri_triet = vi_tri
            else:
                self.diaban[vi_tri - 1].add_star(sao)

        self._init_name()
        self._init_cung_than()
        self._init_zodiac()
        self._init_daihan()
        self._init_tieuhan()
        self._init_nguyethan()
        self._init_sort()

    
    def _init_sort(self) -> None:
        for i in range(12):
            self.diaban[i].chinh_tinh.sort(key=lambda k: k.order)
            self.diaban[i].phu_tinh_trai.sort(key=lambda k: k.order)
            self.diaban[i].phu_tinh_phai.sort(key=lambda k: k.order)


    def _init_name(self) -> None:
        vi_tri_menh = TuViUtil.tim_vi_tri_menh(self.birthdate)
        vi_tri_phu_mau = TuViUtil.tim_cung_phu_mau(self.birthdate)
        vi_tri_phuc_duc = TuViUtil.tim_cung_phuc_duc(self.birthdate)
        vi_tri_dien_trach = TuViUtil.tim_cung_dien_trach(self.birthdate)
        vi_tri_quan_loc = TuViUtil.tim_cung_quan_loc(self.birthdate)
        vi_tri_no_boc = TuViUtil.tim_cung_no_boc(self.birthdate)
        vi_tri_thien_di = TuViUtil.tim_cung_thien_di(self.birthdate)
        vi_tri_tat_ach = TuViUtil.tim_cung_tat_ach(self.birthdate)
        vi_tri_tai_bach = TuViUtil.tim_cung_tai_bach(self.birthdate)
        vi_tri_tu_tuc = TuViUtil.tim_cung_tu_tuc(self.birthdate)
        vi_tri_phu_the = TuViUtil.tim_cung_phu_the(self.birthdate)
        vi_tri_huynh_de = TuViUtil.tim_cung_huynh_de(self.birthdate)

        self.diaban[vi_tri_menh - 1].name = 'MỆNH'
        self.diaban[vi_tri_phu_mau - 1].name = 'PHỤ MẪU'
        self.diaban[vi_tri_phuc_duc - 1].name = 'PHÚC'
        self.diaban[vi_tri_dien_trach - 1].name = 'ĐIỀN TRẠCH'
        self.diaban[vi_tri_quan_loc - 1].name = 'QUAN LỘC'
        self.diaban[vi_tri_no_boc - 1].name = 'NÔ BỘC'
        self.diaban[vi_tri_thien_di - 1].name = 'THIÊN DI'
        self.diaban[vi_tri_tat_ach - 1].name = 'TẬT ÁCH'
        self.diaban[vi_tri_tai_bach - 1].name = 'TÀI BẠCH'
        self.diaban[vi_tri_tu_tuc - 1].name = 'TỬ TỨC'
        
        if self.gender == GioiTinh.NAM.value:
            self.diaban[vi_tri_phu_the - 1].name = 'THÊ'
        elif self.gender == GioiTinh.NU.value:
            self.diaban[vi_tri_phu_the - 1].name = 'PHU'
        else:
            raise InvalidGioiTinh('Gioi tinh khong hop le.')
        
        self.diaban[vi_tri_huynh_de - 1].name = 'HUYNH ĐỆ'


    def _init_cung_than(self) -> None:
        vi_tri_than = TuViUtil.tim_vi_tri_than(self.birthdate)
        self.diaban[vi_tri_than - 1].cung_than = True
        self.diaban[vi_tri_than - 1].name += ' <THÂN>'


    def _init_zodiac(self) -> None:
        lunar_date = DateUtil.solar_to_lunar(self.birthdate.empty_hms())
        can_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[0]
        can_start = (can_nam * 2 + 1) % 10

        self.diaban[0].zodiac = self._transform_zodiac_str(self._get_localized_zodiac(Can(can_start).name.capitalize() + ' ' + Chi(1).name.capitalize()))
        self.diaban[1].zodiac = self._transform_zodiac_str(self._get_localized_zodiac(Can(can_start % 10 + 1).name.capitalize() + ' ' + Chi(2).name.capitalize()))
        self.diaban[2].zodiac = self._transform_zodiac_str(self._get_localized_zodiac(Can(can_start).name.capitalize() + ' ' + Chi(3).name.capitalize()))
        self.diaban[3].zodiac = self._transform_zodiac_str(self._get_localized_zodiac(Can(can_start % 10 + 1).name.capitalize() + ' ' + Chi(4).name.capitalize()))
        for i in range(4, 12):
            self.diaban[i].zodiac = self._transform_zodiac_str(self._get_localized_zodiac(Can((can_start + i - 3) % 10 + 1).name.capitalize() + ' ' + Chi(i + 1).name.capitalize()))


    def _init_daihan(self) -> None:
        am_duong = TuViUtil.tim_am_duong(self.birthdate, self.gender)
        if am_duong in ['Dương Nam', 'Âm Nữ']:
            d = 1
        else:
            d = -1

        cuc = TuViUtil.tim_cuc(self.birthdate)
        if cuc == 'Thuỷ nhị cục':
            start_num = 2
        elif cuc == 'Mộc tam cục':
            start_num = 3
        elif cuc == 'Kim tứ cục':
            start_num = 4
        elif cuc == 'Thổ ngũ cục':
            start_num = 5
        else:
            start_num = 6

        
        vi_tri_menh = TuViUtil.tim_vi_tri_menh(self.birthdate)
        for i in range(12):
            self.diaban[(vi_tri_menh - 1 + d * i + 12) % 12].dai_han = start_num + i * 10

    
    def _init_tieuhan(self) -> None:
        lunar_date = DateUtil.solar_to_lunar(self.birthdate.empty_hms())
        chi_nam = ZodiacUtil.zodiac_year_tuple(lunar_date)[1]
        if chi_nam in [3, 7, 11]:
            cung_bat_dau = 5
        elif chi_nam in [1, 5, 9]:
            cung_bat_dau = 11
        elif chi_nam in [2, 6, 10]:
            cung_bat_dau = 8
        elif chi_nam in [4, 8, 12]:
            cung_bat_dau = 2
        else:
            raise Exception('Chi khong hop le.')
        
        am_duong = TuViUtil.tim_am_duong(self.birthdate, self.gender)
        if am_duong in ['Dương Nam', 'Âm Nam']:
            d = 1
        else:
            d = -1

        cung_ty = (cung_bat_dau - 1 - d * (chi_nam - 1) + 12) % 12 + 1
        for i in range(12):
            self.diaban[(cung_ty - 1 + d * i + 12) % 12].tieu_han = self._get_localized_zodiac(Chi(i + 1).name.capitalize())


    def _init_nguyethan(self) -> None:
        lunar_date = DateUtil.solar_to_lunar(self.birthdate.empty_hms())
        chi_nam_xem = ZodiacUtil.zodiac_year_tuple(Date(self.cur_year, 6, 1))[1]
        chi_gio = ZodiacUtil.zodiac_hour_tuple(self.birthdate)[1]
        ten_chi_nam_xem = self._get_localized_zodiac(Chi(chi_nam_xem).name.capitalize())

        for i in range(12):
            if self.diaban[i].tieu_han == ten_chi_nam_xem:
                pos = i
                break

        vi_tri_thang_1 = (pos - (lunar_date.month - 1) + (chi_gio - 1) + 12) % 12 + 1
        for i in range(12):
            self.diaban[(vi_tri_thang_1 - 1 + i) % 12].nguyet_han = f'Tháng {i + 1}'

    
    @VNLocalizer.localizer
    def _get_localized_zodiac(self, s: str) -> str:
        return s
    

    def _transform_zodiac_str(self, zodiac: str) -> str:
        can, chi = zodiac.split()
        return can[0] + '. ' + chi

    
    def get_image(self) -> str:
        """
        Return horoscope image, in the format of base64 encoded byte string. 
        """
        
        # Define image size and background color
        width, height = 800, 800
        background_color = Color.BACKGROUND.value

        # Create a new image with the specified size and background color
        image = Image.new('RGB', (width, height), background_color)

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Create fonts
        font_path = 'fonts/Arial.ttf'
        bold_font_path = 'fonts/Arial Bold.ttf'
        font_small = ImageFont.truetype(font_path, FontSize.SMALL.value)
        font_medium = ImageFont.truetype(font_path, FontSize.MEDIUM.value)
        font_large = ImageFont.truetype(font_path, FontSize.LARGE.value)
        font_small_bold = ImageFont.truetype(bold_font_path, FontSize.SMALL.value)
        font_medium_bold = ImageFont.truetype(bold_font_path, FontSize.MEDIUM.value)
        font_large_bold = ImageFont.truetype(bold_font_path, FontSize.LARGE.value)

        # Cell width and height
        cell_size = 200
        cell_width, cell_height = cell_size, cell_size

        # Start drawing
        ##### VE DIA BAN #####
        for i in range(12):
            coor = self.diaban[i].coor
            topleft_cell = (coor[1] * cell_width, coor[0] * cell_height)

            # Draw border
            draw.line([topleft_cell, (topleft_cell[0] + cell_width, topleft_cell[1])], fill=Color.BLACK.value, width=2)
            draw.line([topleft_cell, (topleft_cell[0], topleft_cell[1] + cell_height)], fill=Color.BLACK.value, width=2)
            draw.line([(topleft_cell[0] + cell_width, topleft_cell[1]), (topleft_cell[0] + cell_width, topleft_cell[1] + cell_height)], fill=Color.BLACK.value, width=2)
            draw.line([(topleft_cell[0], topleft_cell[1] + cell_height), (topleft_cell[0] + cell_width, topleft_cell[1] + cell_height)], fill=Color.BLACK.value, width=2)
            if i == 0:
                draw.line([(cell_width * 4 - 2, 0), (cell_width * 4 - 2, cell_height * 4 - 2)], fill=Color.BLACK.value, width=2)
                draw.line([(0, cell_height * 4 - 2), (cell_width * 4 - 2, cell_height * 4 - 2)], fill=Color.BLACK.value, width=2)

            # Draw 4 corners
            # Upper left
            draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=5, height_percent=5), self.diaban[i].zodiac, fill=get_color(self.diaban[i].ID), font=font_small_bold)

            # Upper right
            draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=90, height_percent=5), str(self.diaban[i].dai_han), fill=Color.BLACK.value, font=font_small_bold)
            
            # Lower left
            draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=5, height_percent=90), self.diaban[i].tieu_han, fill=Color.BLACK.value, font=font_small)

            # Lower right
            draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=75, height_percent=90), self.diaban[i].nguyet_han, fill=Color.BLACK.value, font=font_small)

            # Draw name and bottom star
            # Name
            text_width, _ = draw.textsize(self.diaban[i].name, font=font_medium_bold)
            draw.text(((cell_width - text_width) // 2 + topleft_cell[0], 10 + topleft_cell[1]), self.diaban[i].name, fill=Color.BLACK.value, font=font_medium_bold)

            # Bottom star
            text_width, _ = draw.textsize(self.diaban[i].phu_tinh_duoi.name, font=font_medium_bold)
            draw.text(((cell_width - text_width) // 2 + topleft_cell[0], cell_height - 25 + topleft_cell[1]), self.diaban[i].phu_tinh_duoi.name, fill=Color.BLACK.value, font=font_medium_bold)

            # Ve chinh tinh
            for j, star in enumerate(self.diaban[i].chinh_tinh):
                cur_name = star.name
                if star.trang_thai.value is not None:
                    cur_name += f'({star.trang_thai.value})'

                text_width, _ = draw.textsize(cur_name, font=font_large_bold)
                draw.text(((cell_width - text_width) // 2 + topleft_cell[0], 25 + 15 * j + topleft_cell[1]), cur_name, fill=get_color_by_nguhanh(star.ngu_hanh.value), font=font_large_bold)
            

            # Ve phu tinh trai
            for j, star in enumerate(self.diaban[i].phu_tinh_trai):
                cur_name = star.name
                if star.trang_thai.value is not None:
                    cur_name += f'({star.trang_thai.value})'

                if star.is_print_bold:
                    draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=5, height_percent=30 + 6 * j), cur_name, fill=get_color_by_nguhanh(star.ngu_hanh.value), font=font_small_bold)
                else:
                    draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=5, height_percent=30 + 6 * j), cur_name, fill=get_color_by_nguhanh(star.ngu_hanh.value), font=font_small)
            
            # Ve phu tinh phai
            for j, star in enumerate(self.diaban[i].phu_tinh_phai):
                cur_name = star.name
                if star.trang_thai.value is not None:
                    cur_name += f'({star.trang_thai.value})'

                if star.is_print_bold:
                    draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=50, height_percent=30 + 6 * j), cur_name, fill=get_color_by_nguhanh(star.ngu_hanh.value), font=font_small_bold)
                else:
                    draw.text(get_position(topleft_cell, (cell_width, cell_height), width_percent=50, height_percent=30 + 6 * j), cur_name, fill=get_color_by_nguhanh(star.ngu_hanh.value), font=font_small)

        # Ve Tuan, Triet
        if self.vi_tri_tuan == self.vi_tri_triet:
            box_width, box_height = 80, 12
            if self.vi_tri_triet == 1:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=75)
            elif self.vi_tri_triet == 3:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=75)
            elif self.vi_tri_triet == 5:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=25)
            elif self.vi_tri_triet == 7:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=25)
            elif self.vi_tri_triet == 9:
                center_box_coor = get_position((0, 0), (width, height), width_percent=87.5, height_percent=25)
            else:
                raise InvalidViTri('Vi tri triet khong hop le.')
            
            topleft_box_coor = (center_box_coor[0] - box_width // 2, center_box_coor[1] - box_height // 2)
            draw.rectangle((*topleft_box_coor, center_box_coor[0] + box_width // 2, center_box_coor[1] + box_height // 2), fill=Color.BLACK.value)
            
            text_width, text_height = draw.textsize('Tuần - Triệt', font=font_small_bold)
            draw.text((center_box_coor[0] - text_width // 2, center_box_coor[1] - text_height // 2 - 2), 'Tuần - Triệt', fill=Color.WHITE.value, font=font_small_bold)
        else:
            box_width, box_height = 50, 12
            # Ve Triet
            if self.vi_tri_triet == 1:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=75)
            elif self.vi_tri_triet == 3:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=75)
            elif self.vi_tri_triet == 5:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=25)
            elif self.vi_tri_triet == 7:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=25)
            elif self.vi_tri_triet == 9:
                center_box_coor = get_position((0, 0), (width, height), width_percent=87.5, height_percent=25)
            else:
                raise InvalidViTri('Vi tri triet khong hop le.')
            
            topleft_box_coor = (center_box_coor[0] - box_width // 2, center_box_coor[1] - box_height // 2)
            draw.rectangle((*topleft_box_coor, center_box_coor[0] + box_width // 2, center_box_coor[1] + box_height // 2), fill=Color.BLACK.value)
            
            text_width, text_height = draw.textsize('Triệt', font=font_small_bold)
            draw.text((center_box_coor[0] - text_width // 2, center_box_coor[1] - text_height // 2), 'Triệt', fill=Color.WHITE.value, font=font_small_bold)

            # Ve Tuan
            if self.vi_tri_tuan == 1:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=75)
            elif self.vi_tri_tuan == 3:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=75)
            elif self.vi_tri_tuan == 5:
                center_box_coor = get_position((0, 0), (width, height), width_percent=12.5, height_percent=25)
            elif self.vi_tri_tuan == 7:
                center_box_coor = get_position((0, 0), (width, height), width_percent=50, height_percent=25)
            elif self.vi_tri_tuan == 9:
                center_box_coor = get_position((0, 0), (width, height), width_percent=87.5, height_percent=25)
            elif self.vi_tri_tuan == 11:
                center_box_coor = get_position((0, 0), (width, height), width_percent=87.5, height_percent=75)
            else:
                raise InvalidViTri('Vi tri tuan khong hop le.')
            
            topleft_box_coor = (center_box_coor[0] - box_width // 2, center_box_coor[1] - box_height // 2)
            draw.rectangle((*topleft_box_coor, center_box_coor[0] + box_width // 2, center_box_coor[1] + box_height // 2), fill=Color.BLACK.value)
            
            text_width, text_height = draw.textsize('Tuần', font=font_small_bold)
            draw.text((center_box_coor[0] - text_width // 2, center_box_coor[1] - text_height // 2), 'Tuần', fill=Color.WHITE.value, font=font_small_bold)
        ##### VE DIA BAN #####

        ##### VE THIEN BAN #####
        # LA SO TU VI
        text_width, text_height = draw.textsize('LÁ SỐ TỬ VI', font=font_large_bold)
        position = get_position((0, 0), (width, height), width_percent=50, height_percent=30)
        draw.text((position[0] - text_width // 2, position[1] - text_height // 2), 'LÁ SỐ TỬ VI', fill=Color.BLUE.value, font=font_large_bold)

        # Ho ten
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=35), 'Họ tên:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=35), self.hoten, fill=Color.BLUE.value, font=font_small)

        # Ngay, Thang, Nam, Gio
        lunar_date = DateUtil.solar_to_lunar(self.birthdate.empty_hms())
        # Nam
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=38), 'Năm:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=38), str(self.old_year), fill=Color.BLUE.value, font=font_small)
        draw.text(get_position((0, 0), (width, height), width_percent=60, height_percent=38), ZodiacUtil.zodiac_year(lunar_date), fill=Color.BLUE.value, font=font_small)
        
        # Thang
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=40), 'Tháng:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=40), f'{str(self.old_month).zfill(2)} ({str(lunar_date.month).zfill(2)})', fill=Color.BLUE.value, font=font_small)
        draw.text(get_position((0, 0), (width, height), width_percent=60, height_percent=40), ZodiacUtil.zodiac_month(lunar_date), fill=Color.BLUE.value, font=font_small)
        
        # Ngay
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=42), 'Ngày:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=42), f'{str(self.old_day).zfill(2)} ({str(lunar_date.day).zfill(2)})', fill=Color.BLUE.value, font=font_small)
        draw.text(get_position((0, 0), (width, height), width_percent=60, height_percent=42), ZodiacUtil.zodiac_day(self.birthdate), fill=Color.BLUE.value, font=font_small)
        
        # Gio
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=44), 'Giờ:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=44), f'{str(self.old_hour).zfill(2)} giờ {str(self.old_minute).zfill(2)} phút', fill=Color.BLUE.value, font=font_small)
        draw.text(get_position((0, 0), (width, height), width_percent=60, height_percent=44), ZodiacUtil.zodiac_hour(self.birthdate), fill=Color.BLUE.value, font=font_small)
        
        # Nam xem
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=47), 'Năm xem:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=47), str(self.cur_year), fill=Color.BLUE.value, font=font_small)
        draw.text(get_position((0, 0), (width, height), width_percent=60, height_percent=47), ZodiacUtil.zodiac_year(Date(self.cur_year, 6, 1)), fill=Color.BLUE.value, font=font_small)
        
        # Tuoi
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=50), f'{self.cur_year - lunar_date.year + 1} tuổi', fill=Color.BLUE.value, font=font_small)

        # Am Duong
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=54), 'Âm Dương:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=54), TuViUtil.tim_am_duong(self.birthdate, self.gender), fill=Color.BLUE.value, font=font_small)

        # Menh
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=56), 'Mệnh:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=56), TuViUtil.tim_menh(self.birthdate), fill=Color.BLUE.value, font=font_small)

        # Cuc
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=58), 'Cục:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=58), TuViUtil.tim_cuc(self.birthdate), fill=Color.BLUE.value, font=font_small)

        # Chu Menh
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=62), 'Chủ Mệnh:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=62), TuViUtil.tim_chu_menh(self.birthdate), fill=Color.BLUE.value, font=font_small)

        # Chu Than
        draw.text(get_position((0, 0), (width, height), width_percent=31.25, height_percent=64), 'Chủ Thân:', fill=Color.BLACK.value, font=font_small_bold)
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=64), TuViUtil.tim_chu_than(self.birthdate), fill=Color.BLUE.value, font=font_small)

        # Tinh ly am duong
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=67), TuViUtil.tim_tinh_ly_am_duong(self.birthdate), fill=Color.BLUE.value, font=font_small_bold)

        # Tinh sinh khac cuc menh
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=69), TuViUtil.tim_cuc_menh_sinh_khac(self.birthdate), fill=Color.BLUE.value, font=font_small_bold)

        # Noi cu than
        draw.text(get_position((0, 0), (width, height), width_percent=43.75, height_percent=71), TuViUtil.tim_noi_cu_than(self.birthdate, self.gender), fill=Color.BLUE.value, font=font_small_bold)

        # Ve tam giac menh - tai - quan
        position_dict = {
            1: get_position((0, 0), (width, height), width_percent=62.5, height_percent=75),
            2: get_position((0, 0), (width, height), width_percent=37.5, height_percent=75),
            3: get_position((0, 0), (width, height), width_percent=25, height_percent=75),
            4: get_position((0, 0), (width, height), width_percent=25, height_percent=62.5),
            5: get_position((0, 0), (width, height), width_percent=25, height_percent=37.5),
            6: get_position((0, 0), (width, height), width_percent=25, height_percent=25),
            7: get_position((0, 0), (width, height), width_percent=37.5, height_percent=25),
            8: get_position((0, 0), (width, height), width_percent=62.5, height_percent=25),
            9: get_position((0, 0), (width, height), width_percent=75, height_percent=25),
            10: get_position((0, 0), (width, height), width_percent=75, height_percent=37.5),
            11: get_position((0, 0), (width, height), width_percent=75, height_percent=62.5),
            12: get_position((0, 0), (width, height), width_percent=75, height_percent=75),
        }

        vi_tri_cung_menh = TuViUtil.tim_vi_tri_menh(self.birthdate)
        vi_tri_cung_tai_bach = TuViUtil.tim_cung_tai_bach(self.birthdate)
        vi_tri_cung_quan_loc = TuViUtil.tim_cung_quan_loc(self.birthdate)

        menh_coor = position_dict.get(vi_tri_cung_menh)
        tai_coor = position_dict.get(vi_tri_cung_tai_bach)
        quan_coor = position_dict.get(vi_tri_cung_quan_loc)

        draw.line([menh_coor, tai_coor], fill=Color.GREY.value, width=1)
        draw.line([menh_coor, quan_coor], fill=Color.GREY.value, width=1)
        draw.line([tai_coor, quan_coor], fill=Color.GREY.value, width=1)
        ##### VE THIEN BAN #####

        # Save image to buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        
        # Set buffer pointer to the beginning
        image_buffer.seek(0)
        
        # Get image byte value
        image_bytes = image_buffer.getvalue()

        # Base64 encoding
        base64_encoded = base64.b64encode(image_bytes).decode()

        return base64_encoded
