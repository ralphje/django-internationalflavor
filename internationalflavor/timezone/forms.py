from django import forms
from .data import get_timezones_cities_lazy, get_metazones_lazy
from internationalflavor.forms import SortedSelect


class TimezoneFormField(forms.TypedChoiceField):
    widget = SortedSelect

    def __init__(self, timezones=None, exclude=None, *args, **kwargs):
        if 'choices' not in kwargs or not kwargs['choices']:
            kwargs['choices'] = get_timezones_cities_lazy(timezones, exclude)

        super(TimezoneFormField, self).__init__(*args, **kwargs)


class MetazoneFormField(forms.TypedChoiceField):
    widget = SortedSelect

    def __init__(self, metazones=None, exclude=None, display_format='name', *args, **kwargs):
        if 'choices' not in kwargs or not kwargs['choices']:
            kwargs['choices'] = get_metazones_lazy(metazones, exclude, display_format=display_format)

        super(MetazoneFormField, self).__init__(*args, **kwargs)
