from django import forms
from .data import COMMON_TIMEZONES, get_timezones_cities_sorted_lazy, get_timezones_cities_sorted


class TimezoneFormField(forms.TypedChoiceField):
    def __init__(self, timezones=None, exclude=(), *args, **kwargs):
        if timezones is None:
            timezones = COMMON_TIMEZONES

        # Maintain the empty choice if available
        if kwargs['choices'] and kwargs['choices'][0][0] == '':
            kwargs['choices'] = [kwargs['choices'][0]] + get_timezones_cities_sorted(timezones, exclude)
        else:
            kwargs['choices'] = get_timezones_cities_sorted_lazy(timezones, exclude)

        super(TimezoneFormField, self).__init__(*args, **kwargs)
