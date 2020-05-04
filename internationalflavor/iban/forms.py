from django import forms
from .data import IBAN_MIN_LENGTH, IBAN_MAX_LENGTH
from internationalflavor.iban.validators import BICValidator, BICCleaner, IBANCleaner, IBANValidator


class IBANFormField(forms.CharField):
    """A form field that applies the :class:`.validators.IBANValidator`. The arguments are equal to those of the
    validator.

    This field represents the data in 4-character blocks, but stores it internally without any formatting.
    """

    def __init__(self, countries=None, exclude=None, sepa_only=False, accept_experimental=False, *args, **kwargs):
        kwargs.setdefault('min_length', IBAN_MIN_LENGTH)
        kwargs.setdefault('max_length', IBAN_MAX_LENGTH)
        self.default_validators = [IBANValidator(countries=countries, exclude=exclude, sepa_only=sepa_only,
                                                 accept_experimental=accept_experimental)]
        super(IBANFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(IBANFormField, self).to_python(value)
        if value is not None:
            return IBANCleaner()(value)
        return value

    def prepare_value(self, value):
        """The display format for IBAN has a space every 4 characters."""
        value = super(IBANFormField, self).prepare_value(value)
        if value is None:
            return value
        return IBANCleaner().display_value(value)


class BICFormField(forms.CharField):
    """A form field that applies the :class:`.validators.BICValidator`."""

    def __init__(self, *args, **kwargs):
        self.default_validators = [BICValidator()]
        super(BICFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(BICFormField, self).to_python(value)
        if value is not None:
            return BICCleaner()(value)
        return value

    def prepare_value(self, value):
        value = super(BICFormField, self).prepare_value(value)
        if value is not None:
            return BICCleaner().display_value(value)
        return value
