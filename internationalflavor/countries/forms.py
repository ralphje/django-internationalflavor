from django import forms
from .data import UN_RECOGNIZED_COUNTRIES, get_countries_lazy


class CountryFormField(forms.CharField):
    def __init__(self, countries=UN_RECOGNIZED_COUNTRIES, exclude=(), *args, **kwargs):
        kwargs.setdefault('min_length', 2)
        kwargs.setdefault('max_length', 2)
        self.choices = get_countries_lazy(countries, exclude)
        super(CountryFormField, self).__init__(*args, **kwargs)
