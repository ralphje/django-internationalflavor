from django import forms
from .data import COMMON_TIMEZONES, get_timezones_cities_sorted_lazy


class TimezoneFormField(forms.TypedChoiceField):
    def __init__(self, timezones=None, exclude=(), *args, **kwargs):
        if timezones is None:
            timezones = COMMON_TIMEZONES

        kwargs['choices'] = get_timezones_cities_sorted_lazy(timezones, exclude)
        super(TimezoneFormField, self).__init__(*args, **kwargs)
