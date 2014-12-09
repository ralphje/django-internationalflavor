from django.db import models
from django.utils.translation import ugettext_lazy as _
from .forms import VATNumberFormField
from .data import VAT_MAX_LENGTH
from .validators import VATNumberValidator


class VATNumberField(models.CharField):
    """A model field that applies the :class:`.validators.VATNumberValidator` and is represented by a
    :class:`.forms.VATNumberFormField`. The arguments are equal to those of the validator.

    Example:

    .. code-block:: python

        from django.db import models
        from internationalflavor.vat_number import VATNumberField

        class MyModel(models.Model):
            vat_number = VATNumberField(include_countries=['NL', 'BE'])

    This field is an extension of a CharField.
    """

    description = _('A number used for VAT registration')

    def __init__(self, eu_only=False, include_countries=None, vies_check=False, *args, **kwargs):
        self.eu_only = eu_only
        self.include_countries = include_countries
        self.vies_check = vies_check

        kwargs.setdefault('max_length', VAT_MAX_LENGTH)
        super(VATNumberField, self).__init__(*args, **kwargs)
        self.validators.append(VATNumberValidator(eu_only=eu_only, include_countries=include_countries,
                                                  vies_check=vies_check))

    def deconstruct(self):
        name, path, args, kwargs = super(VATNumberField, self).deconstruct()
        if self.eu_only:
            kwargs['eu_only'] = self.eu_only
        if self.include_countries:
            kwargs['include_countries'] = self.include_countries
        if self.vies_check:
            kwargs['vies_check'] = self.vies_check
        if 'max_length' in kwargs and kwargs["max_length"] == VAT_MAX_LENGTH:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        value = super(VATNumberField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '').replace('.', '')
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': VATNumberFormField}
        defaults.update(kwargs)
        return super(VATNumberField, self).formfield(**defaults)
