# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.iban import IBANValidator, IBANFormField, IBANField, BICValidator, BICFormField, BICField


class IBANTestCase(TestCase):
    # Note: use https://www.swift.com/resource/iban-registry-txt
    swift_iban_examples = [
        "AD1200012030200359100100",
        "AE070331234567890123456",
        "AL47212110090000000235698741",
        "AT611904300234573201",
        "AZ21NABZ00000000137010001944",
        "BA391290079401028494",
        "BE68539007547034",
        "BG80BNBG96611020345678",
        "BH67BMAG00001299123456",
        "BR1800360305000010009795493C1",
        "BY13NBRB3600900000002Z00AB00",
        "CH9300762011623852957",
        "CR05015202001026284066",
        "CY17002001280000001200527600",
        "CZ6508000000192000145399",
        "DE89370400440532013000",
        "DK5000400440116243",
        "DO28BAGR00000001212453611324",
        "EE382200221020145685",
        "EG380019000500000000263180002",
        "ES9121000418450200051332",
        "FI2112345600000785",
        "FO6264600001631634",
        "FR1420041010050500013M02606",
        "GB29NWBK60161331926819",
        "GE29NB0000000101904917",
        "GI75NWBK000000007099453",
        "GL8964710001000206",
        "GR1601101250000000012300695",
        "GT82TRAJ01020000001210029690",
        "HR1210010051863000160",
        "HU42117730161111101800000000",
        "IE29AIBK93115212345678",
        "IL620108000000099999999",
        "IQ98NBIQ850123456789012",
        "IS140159260076545510730339",
        "IT60X0542811101000000123456",
        "JO94CBJO0010000000000131000302",
        "KW81CBKU0000000000001234560101",
        "KZ86125KZT5004100100",
        "LB62099900000001001901229114",
        "LC55HEMM000100010012001200023015",
        "LI21088100002324013AA",
        "LT121000011101001000",
        "LU280019400644750000",
        "LV80BANK0000435195001",
        "MC5811222000010123456789030",
        "MD24AG000225100013104168",
        "ME25505000012345678951",
        "MK07250120000058984",
        "MR1300020001010000123456753",
        "MT84MALT011000012345MTLCAST001S",
        "MU17BOMM0101101030300200000MUR",
        "NL91ABNA0417164300",
        "NO9386011117947",
        "PK36SCBL0000001123456702",
        "PL61109010140000071219812874",
        "PS92PALS000000000400123456702",
        "PT50000201231234567890154",
        "QA58DOHB00001234567890ABCDEFG",
        "RO49AAAA1B31007593840000",
        "RS35260005601001611379",
        "SA0380000000608010167519",
        "SC18SSCB11010000000000001497USD",
        "SE4550000000058398257466",
        "SI56263300012039086",
        "SK3112000000198742637541",
        "SM86U0322509800000000270100",
        # "ST68000200010192194210112",  # this one has an invalid checksum
        "SV62CENR00000000000000700025",
        "TL380080012345678910157",
        "TN5910006035183598478831",
        "TR330006100519786457841326",
        "UA213223130000026007233566001",
        "VA59001123000012345678",
        "VG96VPVG0000012345678901",
        "XK051212012345678906",
    ]

    swift_experimental_examples = [
        "AO06004400006729503010102",
        "BF42BF0840101300463574000390",
        "BI43201011067444",
        "BJ66BJ0610100100144390000769",
        "CF4220001000010120069700160",
        "CG3930011000101013451300019",
        "CI93CI0080111301134291200589",
        "CM2110002000300277976315008",
        "CV64000500000020108215144",
        "DJ2110002010010409943020008",
        "DZ580002100001113000000570",
        "GA2140021010032001890020126",
        "GQ7050002001003715228190196",
        "GW04GW1430010181800637601",
        "HN54PISA00000000000000123124",
        "IR710570029971601460641001",
        "KM4600005000010010904400137",
        "MA64011519000001205000534921",
        "MG4600005030071289421016045",
        "ML13ML0160120102600100668497",
        "MZ59000301080016367102371",
        "NE58NE0380100100130305000268",
        "NI92BAMC000000000000000003123123",
        "SN08SN0100152000048500003035",
        "TD8960002000010271091600153",
        "TG53TG0090604310346500400070",
    ]

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
        'TR330006100519786457841326': 'TR330006100519786457841326',
        'KW81CBKU0000000000001234560101': 'KW81CBKU0000000000001234560101',
        'ST68000100010051845310112': 'ST68000100010051845310112',
        'MD24AG000225100013104168': 'MD24AG000225100013104168',
        'UA213996220000026007233566001': 'UA213996220000026007233566001',
        'JO94CBJO0010000000000131000302': 'JO94CBJO0010000000000131000302',
        'KZ86125KZT5004100100': 'KZ86125KZT5004100100',
        'PL61109010140000071219812874': 'PL61109010140000071219812874',
        'SC18SSCB11010000000000001497USD': 'SC18SSCB11010000000000001497USD',
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
        # only valid for experimental
        'NI92BAMC000000000000000003123123': ['NI IBANs are not allowed in this field.'],
    }

    def test_iban_examples_from_swift(self):
        validator = IBANValidator()

        for iban in self.swift_iban_examples:
            with self.subTest(iban):
                validator(iban)

    def test_experimental_iban_examples_from_swift(self):
        validator = IBANValidator(accept_experimental=True)

        for iban in self.swift_experimental_examples:
            with self.subTest(iban):
                validator(iban)

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