from django.db import models
from django.utils.translation import ugettext_lazy as _
from .forms import IBANFormField
from .data import IBAN_MAX_LENGTH
from internationalflavor.iban.forms import BICFormField
from .validators import IBANValidator, BICValidator


class IBANField(models.CharField):
    """A model field that applies the :class:`.validators.IBANValidator` and is represented by a
    :class:`.forms.IBANFormField`. The arguments are equal to those of the validator.

    Example:

    .. code-block:: python

        from django.db import models
        from internationalflavor.models import IBANField

        class MyModel(models.Model):
            iban = IBANField(include_countries=['NL', 'BE'])

    This field is an extension of a CharField.
    """

    description = _('An International Bank Account Number')

    def __init__(self, sepa_only=False, include_countries=None, use_nordea_extensions=False, *args, **kwargs):
        self.sepa_only = sepa_only
        self.include_countries = include_countries
        self.use_nordea_extensions = use_nordea_extensions

        kwargs.setdefault('max_length', IBAN_MAX_LENGTH)
        super(IBANField, self).__init__(*args, **kwargs)
        self.validators.append(IBANValidator(sepa_only=sepa_only, include_countries=include_countries,
                                             use_nordea_extensions=use_nordea_extensions))

    def deconstruct(self):
        name, path, args, kwargs = super(IBANField, self).deconstruct()
        if self.sepa_only:
            kwargs['sepa_only'] = self.sepa_only
        if self.include_countries:
            kwargs['include_countries'] = self.include_countries
        if self.use_nordea_extensions:
            kwargs['use_nordea_extensions'] = self.use_nordea_extensions
        if 'max_length' in kwargs and kwargs["max_length"] == IBAN_MAX_LENGTH:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        value = super(IBANField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '')
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': IBANFormField}
        defaults.update(kwargs)
        return super(IBANField, self).formfield(**defaults)


class BICField(models.CharField):
    """A model field that applies the :class:`.validators.BICValidator` and is represented by a
    :class:`.forms.BICFormField`.

    This field is an extension of a CharField.
    """

    description = _('An International Bank Code')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(BICField, self).__init__(*args, **kwargs)
        self.validators.append(BICValidator())

    def deconstruct(self):
        name, path, args, kwargs = super(BICField, self).deconstruct()
        if 'max_length' in kwargs and kwargs["max_length"] == 11:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        value = super(BICField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '')
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': BICFormField}
        defaults.update(kwargs)
        return super(BICField, self).formfield(**defaults)