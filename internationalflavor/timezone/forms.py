from django import forms
from .data import COMMON_TIMEZONES, get_timezones_cities_lazy
from internationalflavor.forms import SortedSelect


class TimezoneFormField(forms.TypedChoiceField):
    widget = SortedSelect

    def __init__(self, timezones=None, exclude=None, *args, **kwargs):
        if 'choices' not in kwargs or not kwargs['choices']:
            kwargs['choices'] = get_timezones_cities_lazy(timezones, exclude)

        super(TimezoneFormField, self).__init__(*args, **kwargs)
