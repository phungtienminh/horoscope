from django import forms
import datetime


class InputForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'pattern': '[a-zA-Z0-9 ]+',
                'title': 'Only letters, numbers and whitespace are allowed.'
            }
        ),
        required=False,
    )

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, initial='M')
    year = forms.ChoiceField(label='Year', choices=[(str(year), str(year)) for year in range(1900, 2100)], initial=str(datetime.datetime.now().year))
    month = forms.ChoiceField(label='Month', choices=[(str(month), str(month)) for month in range(1, 13)])
    day = forms.ChoiceField(label='Day', choices=[(str(day), str(day)) for day in range(1, 32)])
    hour = forms.ChoiceField(label='Hour', choices=[(str(hour), str(hour)) for hour in range(24)])
    minute = forms.ChoiceField(label='Minute', choices=[(str(minute), str(minute)) for minute in range(60)])
    cur_year = forms.ChoiceField(label='Current year', choices=[(str(year), str(year)) for year in range(1900, 2100)], initial=str(datetime.datetime.now().year))
