from django import forms
from .data import VAT_MAX_LENGTH, VAT_MIN_LENGTH
from .validators import VATNumberValidator


class VATNumberFormField(forms.CharField):
    """A form field that applies the :class:`.validators.VATNumberValidator`. The arguments are equal to those of the
    validator.
    """

    def __init__(self, eu_only=False, include_countries=None, vies_check=False, *args, **kwargs):
        kwargs.setdefault('min_length', VAT_MIN_LENGTH)
        kwargs.setdefault('max_length', VAT_MAX_LENGTH)
        self.default_validators = [VATNumberValidator(eu_only=eu_only, include_countries=include_countries,
                                                      vies_check=vies_check)]
        super(VATNumberFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(VATNumberFormField, self).to_python(value)
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '').replace('.', '')
        return value
