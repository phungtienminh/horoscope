from django.urls import path
from . import views

app_name = 'tuvi'

urlpatterns = [
    path('', views.input_form, name='input_form'),
]