from __future__ import absolute_import
from __future__ import unicode_literals

import re
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _
from .data import VAT_NUMBER_REGEXES, EU_VAT_AREA


VIES_CHECK_WSDL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"


class VATNumberValidator(object):
    def __init__(self, eu_only=False, include_countries=None, vies_check=False):
        self.regexes = VAT_NUMBER_REGEXES

        self.vies_check = vies_check
        if self.vies_check:
            eu_only = True

            try:
                import suds
            except ImportError:
                raise ImproperlyConfigured("The VAT VIES check requires suds to be installed.")

        self.included_countries = []
        if eu_only:
            self.included_countries += EU_VAT_AREA
        if include_countries is not None:
            self.included_countries += include_countries

    def __call__(self, value):
        """Validates whether a VAT number validates for a EU country."""
        if value is None:
            return value

        if not re.match("[A-Z]{2}[A-Z0-9]+", value):
            raise ValidationError(_('This VAT number does not start with a country code.'))

        country = value[0:2]
        rest = value[2:]

        if self.included_countries and country not in self.included_countries:
            raise ValidationError(_('%(country)s VAT numbers are not allowed in this field.') % {'country': country})

        country_failure = _('This VAT number does not match the requirements for %(country)s.') % {'country': country}

        try:
            if not re.match(self.regexes[country], rest):
                raise ValidationError(country_failure)
        except KeyError:
            raise ValidationError(_('This VAT number is not for a known country.'))

        # Country specific checks
        if country == 'NL':  # validate against modified elfproef
            total = 0
            for i in range(8):
                total += int(rest[i]) * (9 - i)
            total -= int(rest[8])  # '1' factor is -1 in dutch test
            if total % 11 != 0:
                raise ValidationError(country_failure)

        elif country == 'BE':  # validate with Modulus97 test
            if (97 - (int(rest[0:8]) % 97)) != int(rest[8:10]):
                raise ValidationError(country_failure)

        # Check with WSDL services for valid VAT number
        if self.vies_check:
            try:
                from suds.client import Client
                c = Client(VIES_CHECK_WSDL, timeout=3)
                res = c.service.checkVat(country, rest)
                valid = res.valid is not False
            except Exception:  # may be suds.WebFault, or ImmportError
                valid = True

            if not valid:
                raise ValidationError(_('This VAT number does not exist.'))