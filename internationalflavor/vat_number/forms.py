from django import forms
from .data import VAT_MAX_LENGTH, VAT_MIN_LENGTH
from .validators import VATNumberValidator, VATNumberCleaner


class VATNumberFormField(forms.CharField):
    """A form field that applies the :class:`.validators.VATNumberValidator`. The arguments are equal to those of the
    validator.
    """

    def __init__(self, countries=None, exclude=None, eu_only=False, vies_check=False, *args, **kwargs):
        kwargs.setdefault('min_length', VAT_MIN_LENGTH)
        kwargs.setdefault('max_length', VAT_MAX_LENGTH)
        self.default_validators = [VATNumberValidator(countries=countries, exclude=exclude, eu_only=eu_only,
                                                      vies_check=vies_check)]
        super(VATNumberFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(VATNumberFormField, self).to_python(value)
        if value is not None:
            return VATNumberCleaner()(value)
        return value

    def prepare_value(self, value):
        value = super(VATNumberFormField, self).prepare_value(value)
        if value is not None:
            return VATNumberCleaner().display_value(value)
        return value
