from __future__ import absolute_import
from __future__ import unicode_literals

import re
import socket

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.six.moves.urllib import request

from internationalflavor.validators import UpperCaseValueCleaner
from .data import VAT_NUMBER_REGEXES, EU_VAT_AREA


VIES_CHECK_WSDL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
VIES_CHECK_URL = "http://ec.europa.eu/taxation_customs/vies/services/checkVatService"


class VATNumberCleaner(UpperCaseValueCleaner):
    """Cleaner for VAT numbers"""

    def __call__(self, value):
        if value is not None:
            value = super(VATNumberCleaner, self).__call__(value)
            if value.startswith("CH"):
                if value.startswith("CHE"):
                    value = "CH" + value[3:]
                if value.endswith("MWST"):
                    value = value[:-4]
                elif value.endswith("TVA") or value.endswith("IVA"):
                    value = value[:-3]
            return value
        return value

    def display_value(self, value):
        value = super(VATNumberCleaner, self).display_value(value)
        if value.startswith("CH"):
            value = "CHE" + value[2:]
        return value


class VATNumberValidator(object):
    """Validator for checking whether a given VAT number is valid. A VAT number starts with two characters representing
    the country code, followed by at least 2 characters representing the local VAT number.

    :param countries: If set, the list of accepted origin countries will be limited to the provided list. Otherwise, all
        available VAT number countries are used.

    :param exclude: You can use this parameter to exclude items from the list of countries.

    :param bool eu_only: By default, all countries are allowed. However, if you are an EU company, you are likely to
        only want to accept EU VAT numbers.

    :param bool vies_check: By default, this validator will only validate the syntax of the VAT number. If you need to
        validate using the EU VAT Information Exchange System (VIES) checker (see
        http://ec.europa.eu/taxation_customs/vies/), you can set this boolean. Any VAT number in the EU VAT Area will
        then receive additional validation from the VIES checker, other VAT numbers will be unaffected.

    The VIES check may use two different methods to obtain the result. If the :mod:`suds` module is installed, the VIES
    check uses this module to reach the VIES WSDL services (you could use the ``suds-jurko`` fork for Py3k
    compatibility). If this module is not available, a bare-bones native method is used instead. Both methods should
    give similar results, although using :mod:`suds` should be more reliable.

    .. note::

       If the VIES service can not be reached, this part of the validation will succeed.

    .. note::

       If regulations require you to validate against the VIES service, you probably also want to set ``eu_only``. You
       probably can't accept any other VAT number in that case.

    .. warning::

       The validation of non-EU VAT numbers may be incomplete or wrong in some cases. Please issue a pull request if you
       feel there's an error.
    """

    country_failure = _('This VAT number does not match the requirements for %(country)s.')

    def __init__(self, countries=None, exclude=None, eu_only=False, vies_check=False):
        self.regexes = VAT_NUMBER_REGEXES
        self._wsdl_exception = None

        self.vies_check = vies_check
        if self.vies_check:
            try:
                import suds  # NOQA
            except ImportError:
                self._check_vies = self._check_vies_native
            else:
                self._check_vies = self._check_vies_suds
                del suds  # this suppresses some flake warnings

        countries = self.regexes.keys() if countries is None else countries
        exclude = [] if exclude is None else exclude
        self.countries = [c for c in countries if c not in exclude and (not eu_only or c in EU_VAT_AREA)]

    def __call__(self, value):
        """Validates whether a VAT number validates for a EU country."""
        if value is None:
            return value

        if not re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
            raise ValidationError(_('This VAT number does not start with a country code, or contains invalid '
                                    'characters.'))

        country, rest = value[0:2], value[2:]

        if country not in self.countries:
            raise ValidationError(_('%(country)s VAT numbers are not allowed in this field.') % {'country': country})

        try:
            if not re.match(self.regexes[country], rest):
                raise ValidationError(self.country_failure % {'country': country})
        except KeyError:
            raise ValidationError(_('This VAT number is not for a known country.'))

        # Country specific checks
        self._country_specific_check(country, rest)

        # Check with WSDL services for valid VAT number
        if self.vies_check and country in EU_VAT_AREA:
            self._check_vies(country, rest)

    def _country_specific_check(self, country, rest):
        """Place for country specific validations."""

        if country == 'NL':  # validate against modified elfproef
            total = 0
            for i in range(8):
                total += int(rest[i]) * (9 - i)
            total -= int(rest[8])  # '1' factor is -1 in dutch test
            if total % 11 != 0:
                raise ValidationError(self.country_failure % {'country': country})

        elif country == 'BE':  # validate with Modulus97 test
            if (97 - (int(rest[0:8]) % 97)) != int(rest[8:10]):
                raise ValidationError(self.country_failure % {'country': country})

    def _check_vies_native(self, country, rest):
        envelope = """<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
            xmlns:ns0="urn:ec.europa.eu:taxud:vies:services:checkVat:types"
            xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/>
            <ns1:Body><ns0:checkVat><ns0:countryCode>%s</ns0:countryCode>
            <ns0:vatNumber>%s</ns0:vatNumber></ns0:checkVat></ns1:Body>
            </SOAP-ENV:Envelope>
        """
        try:
            data = envelope % (country, rest)
            req = request.Request(VIES_CHECK_URL, data.encode())
            response = request.urlopen(req)
            result = response.read()

            if b'<valid>false</valid>' in result:
                raise ValidationError(_('This VAT number does not exist.'))

        except IOError as e:
            self._wsdl_exception = e

    def _check_vies_suds(self, country, rest):
        """Method to validate against the VIES WSDL services."""

        import suds
        import suds.client
        import suds.transport

        try:
            c = suds.client.Client(VIES_CHECK_WSDL, timeout=3)
            res = c.service.checkVat(country, rest)
            valid = res.valid is not False
        except (suds.WebFault, suds.transport.TransportError, socket.timeout, OSError, IOError) as e:
            self._wsdl_exception = e
        else:
            if not valid:
                raise ValidationError(_('This VAT number does not exist.'))

    _check_vies = _check_vies_suds
