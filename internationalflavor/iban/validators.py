from __future__ import absolute_import
from __future__ import unicode_literals

import re
import string
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .data import IBAN_REGEXES, NORDEA_IBAN_REGEXES, SEPA_COUNTRIES
from internationalflavor.countries.data import ISO_3166_COUNTRIES


class IBANValidator(object):
    """Validator for checking whether a given IBAN is valid. An IBAN consists of up to 34 alphanumeric characters, where
    the first two characters indicate a country code, the third and fourth indicate a checksum and the rest of the IBAN
    are localized characters (the so-called BBAN).
    
    :param bool sepa_only: By default, all countries are allowed. If you want to reduce the list of countries to the
        list of SEPA countries (i.e. Single European Payments Area), for instance if you are an European company wanting
        to perform direct debits, you can set this to True.
        
    :param include_countries: If set, the list of countries will be limited to the provided list.

    :param bool use_nordea_extensions: By default, this validator will validate any IBAN that is recognized by the 
        SWIFT organization, but Nordea has  specified a few additional IBAN formats. By setting this parameter to True,
        these extensions are also allowed.

    .. warning::

       The validation of the Nordea extensions may be wrong for some countries, as there is no standard for these
       numbers.
    """

    def __init__(self, sepa_only=False, include_countries=None, use_nordea_extensions=False):
        self.regexes = IBAN_REGEXES.copy()
        if use_nordea_extensions:
            self.regexes.update(NORDEA_IBAN_REGEXES)

        self.included_countries = []
        if sepa_only:
            self.included_countries += SEPA_COUNTRIES
        if include_countries is not None:
            self.included_countries += include_countries

    def __call__(self, value):
        if value is None:
            return value

        # Check generic IBAN regex
        if not re.match("[A-Z]{2}[0-9]{2}[A-Z0-9]+", value):
            raise ValidationError(_('This IBAN does not start with a country code and checksum, or contains '
                                    'invalid characters.'))

        country = value[0:2]
        rest = value[2:]

        if self.included_countries and country not in self.included_countries:
            raise ValidationError(_('%(country)s IBANs are not allowed in this field.') % {'country': country})

        try:
            if not re.match(self.regexes[country], rest):
                raise ValidationError(_('This IBAN does not match the requirements for %(country)s.') % {'country': country})
        except KeyError:
            raise ValidationError(_('%(country)s is not a valid country code for IBAN.') % {'country': country})

        # Check checksum
        bban = rest[2:]
        digits = ""
        for character in (bban + country + '00'):
            if character.isdigit():
                digits += character
            else:
                digits += str(ord(character) - ord('A') + 10)
        expected_checksum = string.zfill(str(98 - (int(digits) % 97)), 2)

        if expected_checksum != value[2:4]:
            raise ValidationError(_('This IBAN does not have a valid checksum.'))


class BICValidator(object):
    def __call__(self, value):
        if not re.match("^[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3})?$", value):
            raise ValidationError(_('This Bank Identifier Code (BIC) is invalid.'))
        country = value[4:6]
        if value[4:6] not in ISO_3166_COUNTRIES:
            raise ValidationError(_('%(country)s is not a valid country code.') % {'country': country})