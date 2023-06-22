from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, HttpResponseNotAllowed
from .forms import InputForm

from core.main import LaSoTuVi

import traceback

# Create your views here.

def input_form(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = InputForm()
        return render(request, 'tuvi/input_form.html', {'form': form})
    elif request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                name = cleaned_data.get('name')
                if name is None or name == '':
                    name = 'Tử vi Tiến Minh'
                year = int(cleaned_data.get('year'))
                month = int(cleaned_data.get('month'))
                day = int(cleaned_data.get('day'))
                hour = int(cleaned_data.get('hour'))
                minute = int(cleaned_data.get('minute'))
                cur_year = int(cleaned_data.get('cur_year'))
                gender = cleaned_data.get('gender')
                if gender == 'M':
                    gender = 1
                else:
                    gender = -1

                horoscope = LaSoTuVi(year, month, day, hour, minute, gender=gender, cur_year=cur_year, hoten=name)
                image = horoscope.get_image()
                return render(request, 'tuvi/horoscope.html', {'image': image})
            except Exception as e:
                print(traceback.format_exc())
                return HttpResponseServerError()

        return render(request, 'tuvi/input_form.html', {'form': form})
    else:
        return HttpResponseNotAllowed()
