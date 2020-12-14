from django.db import models
from django.utils.translation import ugettext_lazy as _

from internationalflavor.countries.data import UN_RECOGNIZED_COUNTRIES, get_countries_lazy
from internationalflavor.countries.forms import CountryFormField
from .._helpers import django_3_allowed

if django_3_allowed:
    from django.utils.translation import gettext_lazy as _


class CountryField(models.CharField):
    """A model field that allows users to choose their country. By default, it lists all countries recognized by the UN,
    but using the ``countries`` attribute you can specify your own set of allowed countries. Use ``exclude`` to exclude
    specific countries.
    """

    description = _('A country')

    def __init__(self, countries=None, exclude=None, *args, **kwargs):
        self.countries = UN_RECOGNIZED_COUNTRIES if countries is None else countries
        self.exclude = exclude if exclude else []

        kwargs.setdefault('max_length', 2)
        kwargs['choices'] = get_countries_lazy(countries, exclude)

        super(CountryField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        if self.countries != UN_RECOGNIZED_COUNTRIES:
            kwargs['countries'] = self.countries
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if 'max_length' in kwargs and kwargs["max_length"] == 2:
            del kwargs["max_length"]
        del kwargs["choices"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': CountryFormField}
        defaults.update(kwargs)
        return super(CountryField, self).formfield(**defaults)
