from django import forms
from .data import get_countries_lazy
from internationalflavor.forms import SortedSelect


class CountryFormField(forms.TypedChoiceField):
    """A form field that allows users to choose their country. By default, it lists all countries recognized by the UN,
    but using the ``countries`` attribute you can specify your own set of allowed countries. Use ``exclude`` to exclude
    specific countries.
    """

    widget = SortedSelect

    def __init__(self, countries=None, exclude=None, *args, **kwargs):
        # Maintain the empty choice if available
        if 'choices' not in kwargs or not kwargs['choices']:
            kwargs['choices'] = get_countries_lazy(countries, exclude)

        super(CountryFormField, self).__init__(*args, **kwargs)
