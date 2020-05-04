import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from internationalflavor.validators import UpperCaseValueCleaner, _get_mod97_value
from .data import IBAN_REGEXES, EXPERIMENTAL_IBAN_REGEXES, SEPA_COUNTRIES
from internationalflavor.countries.data import ISO_3166_COUNTRIES


class IBANCleaner(UpperCaseValueCleaner):
    """Cleaner for IBAN"""

    def display_value(self, value):
        """The display format for IBAN has a space every 4 characters."""
        value = super(IBANCleaner, self).display_value(value)
        return ' '.join(value[i:i + 4] for i in range(0, len(value), 4))


class IBANValidator(object):
    """Validator for checking whether a given IBAN is valid. An IBAN consists of up to 34 alphanumeric characters, where
    the first two characters indicate a country code, the third and fourth indicate a checksum and the rest of the IBAN
    are localized characters (the so-called BBAN).

    :param countries: If set, the list of source countries will be limited to the provided list. Otherwise, all
        available IBANs are included (with the exception of experimental IBANs if ``accept_experimental`` is not set).

    :param exclude: You can use this parameter to exclude items from the list of countries.

    :param bool sepa_only: By default, all countries are allowed. If you want to reduce the list of countries to the
        list of SEPA countries (i.e. Single European Payments Area), for instance if you are an European company wanting
        to perform direct debits, you can set this to True. This is equivalent to setting the exclude list to all
        countries without SEPA.

    :param bool accept_experimental: By default, this validator will validate any IBAN that is recognized by the
        SWIFT organization, but SWIFT has specified a few additional IBAN formats and defined them as 'experimental'.
        By setting this parameter to True, these extensions are also allowed.

    .. warning::

       The validation of the experimental numbers may be wrong for some countries, as only their length is published
       by the SWIFT organization
    """

    def __init__(self, countries=None, exclude=None, sepa_only=False, accept_experimental=False):
        self.regexes = IBAN_REGEXES.copy()
        if accept_experimental:
            self.regexes.update(EXPERIMENTAL_IBAN_REGEXES)

        countries = self.regexes.keys() if countries is None else countries
        exclude = [] if exclude is None else exclude
        self.countries = [c for c in countries if c not in exclude and (not sepa_only or c in SEPA_COUNTRIES)]

    def __call__(self, value):
        if value is None:
            return value

        # Check generic IBAN regex
        if not re.match("^[A-Z]{2}[0-9]{2}[A-Z0-9]+$", value):
            raise ValidationError(_('This IBAN does not start with a country code and checksum, or contains '
                                    'invalid characters.'))

        # Check if country code is valid
        country = value[0:2]
        rest = value[2:]

        if country not in self.countries:
            raise ValidationError(_('%(country)s IBANs are not allowed in this field.') % {'country': country})

        try:
            if not re.match(self.regexes[country], rest):
                raise ValidationError(_('This IBAN does not match the requirements for %(country)s.') % {'country': country})
        except KeyError:
            raise ValidationError(_('%(country)s is not a valid country code for IBAN.') % {'country': country})

        # Check checksum
        bban = rest[2:]
        expected_checksum = str(98 - _get_mod97_value(bban + country + '00')).zfill(2)

        if expected_checksum != value[2:4]:
            raise ValidationError(_('This IBAN does not have a valid checksum.'))


class BICCleaner(UpperCaseValueCleaner):
    """Cleaner for BIC"""
    pass


class BICValidator(object):
    def __call__(self, value):
        if not re.match("^[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3})?$", value):
            raise ValidationError(_('This Bank Identifier Code (BIC) is invalid.'))
        country = value[4:6]
        if value[4:6] not in ISO_3166_COUNTRIES:
            raise ValidationError(_('%(country)s is not a valid country code.') % {'country': country})
