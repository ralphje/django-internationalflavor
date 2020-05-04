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
        'NL123456789B13': 'NL123456789B13',

        'DE 114 103 379': 'DE114103379',
        'DE114103379': 'DE114103379',

        'BE 0203.201.340': 'BE0203201340',

        'HU99999999': 'HU99999999',
        'IE1234567XX': 'IE1234567XX',
        'IE1X23456X': 'IE1X23456X',

        'GR123456789': 'EL123456789',

        'CH-123.456.789 MWST': 'CH123456789',
        'CHE-123.456.789 MWST': 'CH123456789',
        'CHE-123.456.789 IVA': 'CH123456789',

        'RU5505035011': 'RU5505035011',
        'RU550501929014': 'RU550501929014',
    }
    invalid = {
        'NL820646661B01': ['This VAT number does not match the requirements for NL.'],
        'BE0203201341': ['This VAT number does not match the requirements for BE.'],
        'DE11410337': ['This VAT number does not match the requirements for DE.'],
        'US123414132': ['US VAT numbers are not allowed in this field.'],
        '123456': ['This VAT number does not start with a country code, or contains invalid characters.'],
        'IE0É12345A': ['This VAT number does not start with a country code, or contains invalid characters.'],
        'RU5505035012': ['This VAT number does not match the requirements for RU.'],
        'RU550501929015': ['This VAT number does not match the requirements for RU.'],
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

    def test_validator_eu_only(self):
        validator = VATNumberValidator(eu_only=True)
        validator('CY12345678A')

    def test_validator_greece(self):
        validator = VATNumberValidator(eu_only=True)
        self.assertRaises(ValidationError, validator, 'GR123456789')
        validator('EL123456789')

        validator = VATNumberValidator(countries=['GR'])
        self.assertRaises(ValidationError, validator, 'GR123456789')
        validator('EL123456789')

        validator = VATNumberValidator(countries=['EL'])
        self.assertRaises(ValidationError, validator, 'GR123456789')
        validator('EL123456789')

    def test_form_field(self):
        self.assertFieldOutput(VATNumberFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = VATNumberFormField()
        self.assertEqual(form_field.prepare_value('DE 114 103 379'), 'DE114103379')
        self.assertEqual(form_field.prepare_value('CHE-123.456.789 IVA'), 'CHE123456789')
        self.assertIsNone(form_field.prepare_value(None))

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
        try:
            with self.assertRaises(ValidationError) as context_manager:
                validator('DE999999999')
            self.assertEqual(context_manager.exception.messages, ['This VAT number does not exist.'])
        except AssertionError:
            # Check if the validation succeeded due to a SUDS error.
            # You should be wary of skipped tests because of this, but the service may also be unavailable at the time.
            if validator._wsdl_exception is not None:
                print("Suds WSDL test skipped due to connection failure")
                self.skipTest("Suds WSDL client failed")
            else:
                raise

    def test_vies_check_validator_native(self):
        validator = VATNumberValidator(vies_check=True)
        validator._check_vies = validator._check_vies_native

        validator('DE114103379')
        try:
            with self.assertRaises(ValidationError) as context_manager:
                validator('DE999999999')
            self.assertEqual(context_manager.exception.messages, ['This VAT number does not exist.'])
        except AssertionError:
            # Check if the validation succeeded due to a SUDS error.
            # You should be wary of skipped tests because of this, but the service may also be unavailable at the time.
            if validator._wsdl_exception is not None:
                print("Native WSDL test skipped due to connection failure")
                self.skipTest("Native WSDL client failed")
            else:
                raise
