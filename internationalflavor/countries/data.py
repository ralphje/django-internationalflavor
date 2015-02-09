# coding=utf-8

"""Although for the most countries, sovereignty is not disputed, there are numerous cases where the definition of
country is not clear. Using the ISO 3166-1 country list may seem the most political correct method, but this would
also include uninhabited wasteland such as Antartica and Norfolk Island. Furthermore, some territories are more or less
part of another country, such as Greenland that is part of Denmark.

To accommodate for these differences, this module chooses to include the following countries in the lists:

- All UN member states
- All UN disputed states (except for when no ISO 3166-1 country code is available)
- All UN observer states
- All UN non-self-governing states (this list is rather arbitrary, unfortunately)

This results in the following ISO 3166-1 territories to be not included:

AQ Antarctica
AX Åland Islands
BL Saint Barthélemy
BQ Bonaire, Sint Eustatius and Saba
BV Bouvet Island
CC Cocos (Keeling) Islands
CW Curaçao
CX Christmas Island
FO Faroe Islands
GF French Guiana
GG Guernsey
GL Greenland
GP Guadeloupe
GS South Georgia and the South Sandwich Islands
HM Heard Island and McDonald Islands
IM Isle of Man
IO British Indian Ocean Territory
JE Jersey
MF Saint Martin (French part)
MO Macao
MP Northern Mariana Islands
MQ Martinique
NF Norfolk Island
PM Saint Pierre and Miquelon
RE Réunion
SJ Svalbard and Jan Mayen
SX Sint Maarten (Dutch part)
TF French Southern Territories
UM United States Minor Outlying Islands
WF Wallis and Futuna
YT Mayotte

The following states are unique to the IOC list, but not included by default in the COUNTRIES constant.

AW Aruba
HK Hong Kong
PR Puerto Rico
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from django.utils.functional import lazy
from ._cldr_data import COUNTRY_NAMES

ISO_3166_COUNTRIES = ('AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ',
                      'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS',
                      'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
                      'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE',
                      'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF',
                      'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM',
                      'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM',
                      'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC',
                      'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK',
                      'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA',
                      'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG',
                      'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW',
                      'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS',
                      'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO',
                      'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI',
                      'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW')
"""All two letter country codes according to ISO 3166-1
Source: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Current_codes
"""

UN_MEMBER_STATES = ('AD', 'AE', 'AF', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF',
                    'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CF', 'CG',
                    'CH', 'CI', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO',
                    'DZ', 'EC', 'EE', 'EG', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH',
                    'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ',
                    'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KZ',
                    'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG',
                    'MH', 'MK', 'ML', 'MM', 'MN', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG',
                    'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK', 'PL', 'PT', 'PW', 'PY',
                    'QA', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SI', 'SK', 'SL', 'SM', 'SN',
                    'SO', 'SR', 'SS', 'ST', 'SV', 'SY', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TM', 'TN', 'TO', 'TR',
                    'TT', 'TV', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS', 'YE', 'ZA', 'ZM',
                    'ZW')
"""List of UN Member States
Source: http://www.un.org/en/members/index.shtml
"""

UN_OBSERVER_STATES = ('PS', 'VA')
"""List of UN Observer States
Source: http://www.un.org/en/members/nonmembers.shtml
"""

UN_DISPUTED_STATES = ('CK', 'NU', 'TW', 'XK')
"""Disputed UN states.

Source: https://en.wikipedia.org/wiki/List_of_sovereign_states#List_of_states

No ISO 3166-1 code has yet been assigned, and thus not included, for:

* Abkhazia
* Nagorno-Karabakh
* Northern Cyprus
* Sahrawi Arab Democratic Republic
* Somaliland
* South Ossetia
* Transnistria

Although Kosovo has no ISO 3166-1 code either, it is generally accepted to be XK temporarily; see
http://ec.europa.eu/budget/contracts_grants/info_contracts/inforeuro/inforeuro_en.cfm or the CLDR
"""

UN_NON_SELF_GOVERNING_STATES = ('EH', 'AI', 'BM', 'VG', 'KY', 'FK', 'MS', 'SH', 'TC', 'VI', 'GI', 'AS', 'PF', 'GU',
                                'NC', 'PN', 'TK')
"""List of the (rather arbitrary) UN non-self-governing states

Source: http://www.un.org/en/decolonization/nonselfgovterritories.shtml
"""

IOC_RECOGNIZED_COUNTRIES = ('AF', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH',
                            'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BA', 'BW', 'BR', 'VG', 'BN', 'BG',
                            'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CO', 'KM', 'CG', 'CD',
                            'CK', 'CR', 'CI', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ',
                            'ER', 'EE', 'ET', 'FJ', 'FI', 'FR', 'GA', 'GM', 'GE', 'DE', 'GH', 'GR', 'GD', 'GU', 'GT',
                            'GN', 'GW', 'GY', 'HT', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IL', 'IT',
                            'JM', 'JP', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR',
                            'LY', 'LI', 'LT', 'LU', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MR', 'MU', 'MX',
                            'FM', 'MD', 'MC', 'MN', 'ME', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NZ', 'NI', 'NE',
                            'NG', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'PR', 'QA',
                            'RO', 'RU', 'RW', 'KN', 'LC', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG',
                            'SK', 'SI', 'SB', 'SO', 'ZA', 'ES', 'LK', 'SD', 'SR', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ',
                            'TZ', 'TH', 'TL', 'TG', 'TO', 'TT', 'TN', 'TR', 'TM', 'TV', 'UG', 'UA', 'AE', 'GB', 'US',
                            'VI', 'UY', 'UZ', 'VU', 'VE', 'VN', 'YE', 'ZM', 'ZW')
"""List of countries as defined by IOC.

Source: https://en.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes
"""

UN_RECOGNIZED_COUNTRIES = UN_MEMBER_STATES + UN_OBSERVER_STATES + UN_NON_SELF_GOVERNING_STATES + UN_DISPUTED_STATES
"""Combined list of all UN_* data constants."""


def get_countries(countries=None, exclude=None):
    """Returns a list of (country code, country name)-pairs.

    Only countries present in the countries argument, and not present in the excluded argument, are returned. If you
    wish, for instance, to list all available countries, you could use
    get_countries(ISO_3166_COUNTRIES)

    If you wish to list all countries recognized by the IOC, but not by the UN, you could use
    get_countries(IOC_RECOGNIZED_COUNTRIES, exclude=UN_RECOGNIZED_COUNTRIES)
    or
    get_countries(set(IOC_RECOGNIZED_COUNTRIES) - set(UN_RECOGNIZED_COUNTRIES))

    By default, only lists all countries recognized by the UN as being a member state, observer state,
    non-self-governing territory or disputed state.
    """
    countries = UN_RECOGNIZED_COUNTRIES if countries is None else countries
    exclude = exclude if exclude else []

    return [(k, v) for k, v in COUNTRY_NAMES.items() if k in countries and k not in exclude]

get_countries_lazy = lazy(get_countries, list)
