# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.vat_number import VATNumberValidator
from internationalflavor.vat_number.forms import VATNumberFormField
from internationalflavor.vat_number.models import VATNumberField


class VATNumberTestCase(TestCase):
    valid = {
        'NL820646660B01': 'NL820646660B01',
        'NL82064-6660.B01': 'NL820646660B01',

        'DE 114 103 379': 'DE114103379',
        'DE114103379': 'DE114103379',

        'BE 0203.201.340': 'BE0203201340',
    }
    invalid = {
        'NL820646661B01': ['This VAT number does not match the requirements for NL.'],
        'BE0203201341': ['This VAT number does not match the requirements for BE.'],
        'DE11410337': ['This VAT number does not match the requirements for DE.'],
        'US123414132': ['US VAT numbers are not allowed in this field.'],
        '123456': ['This VAT number does not start with a country code, or contains invalid characters.'],
        'IE0É12345A': ['This VAT number does not start with a country code, or contains invalid characters.'],
    }

    def test_validator(self):
        validator = VATNumberValidator()

        # Our validator does not allow formatting characters, so check we do not pass it in.
        for iban, cleaned in self.valid.items():
            if iban == cleaned:
                validator(iban)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, iban)

        for iban, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, iban)

    def test_form_field(self):
        self.assertFieldOutput(VATNumberFormField, valid=self.valid, invalid=self.invalid)

    def test_model_field(self):
        model_field = VATNumberField()
        for input, output in self.valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

    include_countries = ('NL', 'BE')
    include_countries_valid = {
        'NL820646660B01': 'NL820646660B01',
        'BE0203201340': 'BE0203201340'
    }
    include_countries_invalid = {
        'DE114103379': ['DE VAT numbers are not allowed in this field.']
    }

    def test_include_countries_form_field(self):
        self.assertFieldOutput(VATNumberFormField, field_kwargs={'countries': self.include_countries},
                               valid=self.include_countries_valid, invalid=self.include_countries_invalid)

    def test_include_countries_model_field(self):
        model_field = VATNumberField(countries=self.include_countries)
        for input, output in self.include_countries_valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in self.include_countries_invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

    def test_vies_check_validator(self):
        validator = VATNumberValidator(vies_check=True)

        validator('DE114103379')
        with self.assertRaises(ValidationError) as context_manager:
            validator('DE999999999')
            # Check if the validation succeeded due to a SUDS error.
            # You should be wary of skipped tests because of this, but the service may also be unavailable at the time.
            if validator._suds_exception is not None:
                print("WSDL test skipped due to connection failure")
                self.skipTest("WSDL client failed")
        self.assertEqual(context_manager.exception.messages, ['This VAT number does not exist.'])