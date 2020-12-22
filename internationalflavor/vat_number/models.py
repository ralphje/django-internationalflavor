from django.db import models

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # for Django version 2
    from django.utils.translation import ugettext_lazy as _

from .forms import VATNumberFormField
from .data import VAT_MAX_LENGTH
from .validators import VATNumberValidator, VATNumberCleaner


class VATNumberField(models.CharField):
    """A model field that applies the :class:`.validators.VATNumberValidator` and is represented by a
    :class:`.forms.VATNumberFormField`. The arguments are equal to those of the validator.

    Example:

    .. code-block:: python

        from django.db import models
        from internationalflavor.vat_number import VATNumberField

        class MyModel(models.Model):
            vat_number = VATNumberField(countries=['NL', 'BE'])

    This field is an extension of a CharField.
    """

    description = _('A number used for VAT registration')

    def __init__(self, countries=None, exclude=None, eu_only=False, vies_check=False, *args, **kwargs):
        self.countries = countries
        self.exclude = exclude
        self.eu_only = eu_only
        self.vies_check = vies_check

        kwargs.setdefault('max_length', VAT_MAX_LENGTH)
        super(VATNumberField, self).__init__(*args, **kwargs)
        self.validators.append(VATNumberValidator(countries=countries, exclude=exclude,  # pylint: disable=E1101
                                                  eu_only=eu_only, vies_check=vies_check))

    def deconstruct(self):
        name, path, args, kwargs = super(VATNumberField, self).deconstruct()
        if self.countries:
            kwargs['countries'] = self.countries
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if self.eu_only:
            kwargs['eu_only'] = self.eu_only
        if self.vies_check:
            kwargs['vies_check'] = self.vies_check
        if 'max_length' in kwargs and kwargs["max_length"] == VAT_MAX_LENGTH:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        value = super(VATNumberField, self).to_python(value)
        if value is not None:
            return VATNumberCleaner()(value)
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': VATNumberFormField}
        defaults.update(kwargs)
        return super(VATNumberField, self).formfield(**defaults)
