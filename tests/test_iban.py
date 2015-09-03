# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.iban import IBANValidator, IBANFormField, IBANField, BICValidator, BICFormField, BICField


class IBANTestCase(TestCase):
    valid = {
        'GB82WeST12345698765432': 'GB82WEST12345698765432',
        'GB82 WEST 1234 5698 7654 32': 'GB82WEST12345698765432',

        'GR1601101250000000012300695': 'GR1601101250000000012300695',
        'GR16-0110-1250-0000-0001-2300-695': 'GR1601101250000000012300695',

        'GB29NWBK60161331926819': 'GB29NWBK60161331926819',
        'GB29N-WB K6016-13319-26819': 'GB29NWBK60161331926819',

        'SA0380000000608010167519': 'SA0380000000608010167519',
        'SA0380 0 0000 06 0 8 0 1 0 1 6 7 519 ': 'SA0380000000608010167519',

        'CH9300762011623852957': 'CH9300762011623852957',
        'IL620108000000099999999': 'IL620108000000099999999',
        'EE982200221111099080': 'EE982200221111099080',

        'NL02ABNA0123456789': 'NL02ABNA0123456789',
        'Nl02aBNa0123456789': 'NL02ABNA0123456789',
        'NL02 ABNA 0123 4567 89': 'NL02ABNA0123456789',
        'NL02-ABNA-0123-4567-89': 'NL02ABNA0123456789',

        'NL91ABNA0417164300': 'NL91ABNA0417164300',
        'NL91 ABNA 0417 1643 00': 'NL91ABNA0417164300',
        'NL91-ABNA-0417-1643-00': 'NL91ABNA0417164300',

        'MU17BOMM0101101030300200000MUR': 'MU17BOMM0101101030300200000MUR',
        'MU17 BOMM 0101 1010 3030 0200 000M UR': 'MU17BOMM0101101030300200000MUR',
        'MU 17BO MM01011010 3030-02 000-00M UR': 'MU17BOMM0101101030300200000MUR',

        'BE68539007547034': 'BE68539007547034',
        'BE68 5390 0754 7034': 'BE68539007547034',
        'BE-685390075470 34': 'BE68539007547034',

        'LC55HEMM000100010012001200023015': 'LC55HEMM000100010012001200023015',
        # the one in the iban registry is invalid
        'TR330006100519786457841326': 'TR330006100519786457841326',
        'KW81CBKU0000000000001234560101': 'KW81CBKU0000000000001234560101',
        'ST68000100010051845310112': 'ST68000100010051845310112'
    }
    invalid = {
        'GB82WEST1234569876543': ['This IBAN does not match the requirements for GB.'],
        'CA34CIBC123425345': ['CA IBANs are not allowed in this field.'],
        'GB29ÉWBK60161331926819': ['This IBAN does not start with a country code and checksum, or contains invalid '
                                   'characters.'],
        '123456': ['This IBAN does not start with a country code and checksum, or contains invalid characters.',
                   'Ensure this value has at least 16 characters (it has 6).'],
        'SA0380000000608019167519': ['This IBAN does not have a valid checksum.'],
        'EE012200221111099080': ['This IBAN does not have a valid checksum.'],

        'NL91ABNB0417164300': ['This IBAN does not have a valid checksum.'],

        'MU17BOMM0101101030300200000MUR12345': ['This IBAN does not match the requirements for MU.',
                                                'Ensure this value has at most 34 characters (it has 35).'],
        # only valid for nordea
        'EG1100006001880800100014553': ['EG IBANs are not allowed in this field.'],
    }

    def test_validator(self):
        validator = IBANValidator()

        # Our validator does not allow formatting characters, so check we do not pass it in.
        for iban, cleaned in self.valid.items():
            if iban == cleaned:
                validator(iban)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, iban)

        for iban, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, iban)

        self.assertRaisesMessage(ValidationError, "This IBAN does not start with a country code and checksum, or "
                                                  "contains invalid characters.", validator, "NL02 ABNA 0123 4567 89")

    def test_form_field(self):
        self.assertFieldOutput(IBANFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = IBANFormField()
        self.assertEqual(form_field.prepare_value('NL02ABNA0123456789'), 'NL02 ABNA 0123 4567 89')
        self.assertEqual(form_field.prepare_value('NL02 ABNA 0123 4567 89'), 'NL02 ABNA 0123 4567 89')
        self.assertIsNone(form_field.prepare_value(None))

    def test_model_field(self):
        iban_model_field = IBANField()
        for input, output in self.valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                iban_model_field.clean(input, None)
            # We can't check against minimum length here :(
            if input == '123456':
                self.assertEqual(context_manager.exception.messages, errors[0:1])
            else:
                # The error messages for models are in a different order.
                self.assertEqual(context_manager.exception.messages, errors[::-1])

    def test_use_nordea_extensions(self):
        validator = IBANValidator(accept_nordea_extensions=True)
        validator('EG1100006001880800100014553')

    include_countries = ('NL', 'BE', 'LU')
    include_countries_valid = {
        'NL02ABNA0123456789': 'NL02ABNA0123456789',
        'BE68539007547034': 'BE68539007547034',
        'LU280019400644750000': 'LU280019400644750000'
    }
    include_countries_invalid = {
        'GB82WEST12345698765432': ['GB IBANs are not allowed in this field.']
    }

    def test_include_countries_form_field(self):
        self.assertFieldOutput(IBANFormField, field_kwargs={'countries': self.include_countries},
                               valid=self.include_countries_valid, invalid=self.include_countries_invalid)

    def test_include_countries_model_field(self):
        iban_model_field = IBANField(countries=self.include_countries)
        for input, output in self.include_countries_valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in self.include_countries_invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                iban_model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])


class BICTestCase(TestCase):
    valid = {
        'deutdeff': 'DEUTDEFF',
        'DEUTDEFF': 'DEUTDEFF',
        'NEDSZAJJxxx': 'NEDSZAJJXXX',
        'NEDSZAJJXXX': 'NEDSZAJJXXX',
        'DABADKKK': 'DABADKKK',
        'daBadKkK': 'DABADKKK',
        'UNCRIT2B912': 'UNCRIT2B912',
        'DSBACNBXSHA': 'DSBACNBXSHA'
    }
    invalid = {
        'NEDSZAJJXX': ['This Bank Identifier Code (BIC) is invalid.'],
        'CIBCJJH2': ['JJ is not a valid country code.'],
        'DÉUTDEFF': ['This Bank Identifier Code (BIC) is invalid.']
    }

    def test_validator(self):
        validator = BICValidator()

        # Our validator does not allow formatting characters, so check we do not pass it in.
        for bic, cleaned in self.valid.items():
            if bic == cleaned:
                validator(bic)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, bic)

        for bic, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, bic)

        self.assertRaisesMessage(ValidationError, "This Bank Identifier Code (BIC) is invalid.", validator, "deutdeff")

    def test_form_field(self):
        self.assertFieldOutput(BICFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = BICFormField()
        self.assertEqual(form_field.prepare_value('deutdeff'), 'DEUTDEFF')
        self.assertIsNone(form_field.prepare_value(None))
        self.assertEqual(form_field.to_python(None), '')

    def test_model_field(self):
        model_field = BICField()
        for input, output in self.valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])