from django import forms
from .data import IBAN_MIN_LENGTH, IBAN_MAX_LENGTH
from internationalflavor.iban.validators import BICValidator
from .validators import IBANValidator


class IBANFormField(forms.CharField):
    """A form field that applies the :class:`.validators.IBANValidator`. The arguments are equal to those of the
    validator.

    This field represents the data in 4-character blocks, but stores it internally without any formatting.
    """

    def __init__(self, sepa_only=False, include_countries=None, use_nordea_extensions=False, *args, **kwargs):
        kwargs.setdefault('min_length', IBAN_MIN_LENGTH)
        kwargs.setdefault('max_length', IBAN_MAX_LENGTH)
        self.default_validators = [IBANValidator(sepa_only=sepa_only, include_countries=include_countries,
                                                 use_nordea_extensions=use_nordea_extensions)]
        super(IBANFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(IBANFormField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '')
        return value

    def prepare_value(self, value):
        """The display format for IBAN has a space every 4 characters."""
        value = super(IBANFormField, self).prepare_value(value)
        if value is None:
            return value
        value = value.upper().replace(' ', '').replace('-', '')
        return ' '.join(value[i:i + 4] for i in range(0, len(value), 4))


class BICFormField(forms.CharField):
    """A form field that applies the :class:`.validators.BICValidator`."""

    def __init__(self, *args, **kwargs):
        self.default_validators = [BICValidator()]
        super(BICFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(BICFormField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '')
        return value

    def prepare_value(self, value):
        value = super(BICFormField, self).prepare_value(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '')
        return value
