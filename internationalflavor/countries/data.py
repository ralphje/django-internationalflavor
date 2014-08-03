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
from django.utils import six
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _

"""All two letter country codes according to ISO 3166-1, with their common names and not their official names
Source: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Current_codes
"""
ISO_3166_COUNTRIES = {"AD": _("Andorra"),
                      "AE": _("United Arab Emirates"),
                      "AF": _("Afghanistan"),
                      "AG": _("Antigua and Barbuda"),
                      "AI": _("Anguilla"),
                      "AL": _("Albania"),
                      "AM": _("Armenia"),
                      "AO": _("Angola"),
                      "AQ": _("Antarctica"),
                      "AR": _("Argentina"),
                      "AS": _("American Samoa"),
                      "AT": _("Austria"),
                      "AU": _("Australia"),
                      "AW": _("Aruba"),
                      "AX": _("Åland Islands"),
                      "AZ": _("Azerbaijan"),
                      "BA": _("Bosnia and Herzegovina"),
                      "BB": _("Barbados"),
                      "BD": _("Bangladesh"),
                      "BE": _("Belgium"),
                      "BF": _("Burkina Faso"),
                      "BG": _("Bulgaria"),
                      "BH": _("Bahrain"),
                      "BI": _("Burundi"),
                      "BJ": _("Benin"),
                      "BL": _("Saint Barthélemy"),
                      "BM": _("Bermuda"),
                      "BN": _("Brunei"),
                      "BO": _("Bolivia"),
                      "BQ": _("Bonaire, Sint Eustatius and Saba"),
                      "BR": _("Brazil"),
                      "BS": _("Bahamas"),
                      "BT": _("Bhutan"),
                      "BV": _("Bouvet Island"),
                      "BW": _("Botswana"),
                      "BY": _("Belarus"),
                      "BZ": _("Belize"),
                      "CA": _("Canada"),
                      "CC": _("Cocos (Keeling) Islands"),
                      "CD": _("Congo, the Democratic Republic of the"),
                      "CF": _("Central African Republic"),
                      "CG": _("Congo"),
                      "CH": _("Switzerland"),
                      "CI": _("Côte d'Ivoire"),
                      "CK": _("Cook Islands"),
                      "CL": _("Chile"),
                      "CM": _("Cameroon"),
                      "CN": _("China"),
                      "CO": _("Colombia"),
                      "CR": _("Costa Rica"),
                      "CU": _("Cuba"),
                      "CV": _("Cape Verde"),
                      "CW": _("Curaçao"),
                      "CX": _("Christmas Island"),
                      "CY": _("Cyprus"),
                      "CZ": _("Czech Republic"),
                      "DE": _("Germany"),
                      "DJ": _("Djibouti"),
                      "DK": _("Denmark"),
                      "DM": _("Dominica"),
                      "DO": _("Dominican Republic"),
                      "DZ": _("Algeria"),
                      "EC": _("Ecuador"),
                      "EE": _("Estonia"),
                      "EG": _("Egypt"),
                      "EH": _("Western Sahara"),
                      "ER": _("Eritrea"),
                      "ES": _("Spain"),
                      "ET": _("Ethiopia"),
                      "FI": _("Finland"),
                      "FJ": _("Fiji"),
                      "FK": _("Falkland Islands (Malvinas)"),
                      "FM": _("Micronesia, Federated States of"),
                      "FO": _("Faroe Islands"),
                      "FR": _("France"),
                      "GA": _("Gabon"),
                      "GB": _("United Kingdom"),
                      "GD": _("Grenada"),
                      "GE": _("Georgia"),
                      "GF": _("French Guiana"),
                      "GG": _("Guernsey"),
                      "GH": _("Ghana"),
                      "GI": _("Gibraltar"),
                      "GL": _("Greenland"),
                      "GM": _("Gambia"),
                      "GN": _("Guinea"),
                      "GP": _("Guadeloupe"),
                      "GQ": _("Equatorial Guinea"),
                      "GR": _("Greece"),
                      "GS": _("South Georgia and the South Sandwich Islands"),
                      "GT": _("Guatemala"),
                      "GU": _("Guam"),
                      "GW": _("Guinea-Bissau"),
                      "GY": _("Guyana"),
                      "HK": _("Hong Kong"),
                      "HM": _("Heard Island and McDonald Islands"),
                      "HN": _("Honduras"),
                      "HR": _("Croatia"),
                      "HT": _("Haiti"),
                      "HU": _("Hungary"),
                      "ID": _("Indonesia"),
                      "IE": _("Ireland"),
                      "IL": _("Israel"),
                      "IM": _("Isle of Man"),
                      "IN": _("India"),
                      "IO": _("British Indian Ocean Territory"),
                      "IQ": _("Iraq"),
                      "IR": _("Iran"),
                      "IS": _("Iceland"),
                      "IT": _("Italy"),
                      "JE": _("Jersey"),
                      "JM": _("Jamaica"),
                      "JO": _("Jordan"),
                      "JP": _("Japan"),
                      "KE": _("Kenya"),
                      "KG": _("Kyrgyzstan"),
                      "KH": _("Cambodia"),
                      "KI": _("Kiribati"),
                      "KM": _("Comoros"),
                      "KN": _("Saint Kitts and Nevis"),
                      "KP": _("North Korea"),
                      "KR": _("South Korea"),
                      "KW": _("Kuwait"),
                      "KY": _("Cayman Islands"),
                      "KZ": _("Kazakhstan"),
                      "LA": _("Laos"),
                      "LB": _("Lebanon"),
                      "LC": _("Saint Lucia"),
                      "LI": _("Liechtenstein"),
                      "LK": _("Sri Lanka"),
                      "LR": _("Liberia"),
                      "LS": _("Lesotho"),
                      "LT": _("Lithuania"),
                      "LU": _("Luxembourg"),
                      "LV": _("Latvia"),
                      "LY": _("Libya"),
                      "MA": _("Morocco"),
                      "MC": _("Monaco"),
                      "MD": _("Moldova"),
                      "ME": _("Montenegro"),
                      "MF": _("Saint Martin (French part)"),
                      "MG": _("Madagascar"),
                      "MH": _("Marshall Islands"),
                      "MK": _("Macedonia, the former Yugoslav Republic o)"),
                      "ML": _("Mali"),
                      "MM": _("Myanmar"),
                      "MN": _("Mongolia"),
                      "MO": _("Macao"),
                      "MP": _("Northern Mariana Islands"),
                      "MQ": _("Martinique"),
                      "MR": _("Mauritania"),
                      "MS": _("Montserrat"),
                      "MT": _("Malta"),
                      "MU": _("Mauritius"),
                      "MV": _("Maldives"),
                      "MW": _("Malawi"),
                      "MX": _("Mexico"),
                      "MY": _("Malaysia"),
                      "MZ": _("Mozambique"),
                      "NA": _("Namibia"),
                      "NC": _("New Caledonia"),
                      "NE": _("Niger"),
                      "NF": _("Norfolk Island"),
                      "NG": _("Nigeria"),
                      "NI": _("Nicaragua"),
                      "NL": _("Netherlands"),
                      "NO": _("Norway"),
                      "NP": _("Nepal"),
                      "NR": _("Nauru"),
                      "NU": _("Niue"),
                      "NZ": _("New Zealand"),
                      "OM": _("Oman"),
                      "PA": _("Panama"),
                      "PE": _("Peru"),
                      "PF": _("French Polynesia"),
                      "PG": _("Papua New Guinea"),
                      "PH": _("Philippines"),
                      "PK": _("Pakistan"),
                      "PL": _("Poland"),
                      "PM": _("Saint Pierre and Miquelon"),
                      "PN": _("Pitcairn"),
                      "PR": _("Puerto Rico"),
                      "PS": _("Palestine, State of"),
                      "PT": _("Portugal"),
                      "PW": _("Palau"),
                      "PY": _("Paraguay"),
                      "QA": _("Qatar"),
                      "RE": _("Réunion"),
                      "RO": _("Romania"),
                      "RS": _("Serbia"),
                      "RU": _("Russia"),
                      "RW": _("Rwanda"),
                      "SA": _("Saudi Arabia"),
                      "SB": _("Solomon Islands"),
                      "SC": _("Seychelles"),
                      "SD": _("Sudan"),
                      "SE": _("Sweden"),
                      "SG": _("Singapore"),
                      "SH": _("Saint Helena, Ascension and Tristan da Cunha"),
                      "SI": _("Slovenia"),
                      "SJ": _("Svalbard and Jan Mayen"),
                      "SK": _("Slovakia"),
                      "SL": _("Sierra Leone"),
                      "SM": _("San Marino"),
                      "SN": _("Senegal"),
                      "SO": _("Somalia"),
                      "SR": _("Suriname"),
                      "SS": _("South Sudan"),
                      "ST": _("Sao Tome and Principe"),
                      "SV": _("El Salvador"),
                      "SX": _("Sint Maarten (Dutch part)"),
                      "SY": _("Syria"),
                      "SZ": _("Swaziland"),
                      "TC": _("Turks and Caicos Islands"),
                      "TD": _("Chad"),
                      "TF": _("French Southern Territories"),
                      "TG": _("Togo"),
                      "TH": _("Thailand"),
                      "TJ": _("Tajikistan"),
                      "TK": _("Tokelau"),
                      "TL": _("Timor-Leste"),
                      "TM": _("Turkmenistan"),
                      "TN": _("Tunisia"),
                      "TO": _("Tonga"),
                      "TR": _("Turkey"),
                      "TT": _("Trinidad and Tobago"),
                      "TV": _("Tuvalu"),
                      "TW": _("Taiwan, Province of China"),
                      "TZ": _("Tanzania"),
                      "UA": _("Ukraine"),
                      "UG": _("Uganda"),
                      "UM": _("United States Minor Outlying Islands"),
                      "US": _("United States"),
                      "UY": _("Uruguay"),
                      "UZ": _("Uzbekistan"),
                      "VA": _("Holy See (Vatican City State)"),
                      "VC": _("Saint Vincent and the Grenadines"),
                      "VE": _("Venezuela"),
                      "VG": _("Virgin Islands, British"),
                      "VI": _("Virgin Islands, U.S."),
                      "VN": _("Vietnam"),
                      "VU": _("Vanuatu"),
                      "WF": _("Wallis and Futuna"),
                      "WS": _("Samoa"),
                      "XK": _("Kosovo"),  # Code used by many organizations to temporarily denote Kosovo
                      "YE": _("Yemen"),
                      "YT": _("Mayotte"),
                      "ZA": _("South Africa"),
                      "ZM": _("Zambia"),
                      "ZW": _("Zimbabwe"),
                      }

"""List of UN Member States
Source: http://www.un.org/en/members/index.shtml
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

"""List of UN Observer States
Source: http://www.un.org/en/members/nonmembers.shtml
"""
UN_OBSERVER_STATES = ('PS', 'VA')

"""Disputed UN states.
Source: https://en.wikipedia.org/wiki/List_of_sovereign_states#List_of_states
No ISO 3166-1 code has yet been assigned, and thus not included, for:
Abkhazia
Nagorno-Karabakh
Northern Cyprus
Sahrawi Arab Democratic Republic
Somaliland
South Ossetia
Transnistria

(Kosovo is included temporarily as XK,
 see http://ec.europa.eu/budget/contracts_grants/info_contracts/inforeuro/inforeuro_en.cfm)
"""
UN_DISPUTED_STATES = ('CK', 'NU', 'TW', 'XK')

"""List of the (rather arbitrary) UN non-self-governing states
Source: http://www.un.org/en/decolonization/nonselfgovterritories.shtml
"""
UN_NON_SELF_GOVERNING_STATES = ('EH', 'AI', 'BM', 'VG', 'KY', 'FK', 'MS', 'SH', 'TC', 'VI', 'GI', 'AS', 'PF', 'GU',
                                'NC', 'PN', 'TK')

"""List of countries as defined by IOC.
Source: https://en.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes
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

UN_RECOGNIZED_COUNTRIES = UN_MEMBER_STATES + UN_OBSERVER_STATES + UN_NON_SELF_GOVERNING_STATES + UN_DISPUTED_STATES


def get_countries(countries=UN_RECOGNIZED_COUNTRIES, exclude=()):
    """Returns a sorted (based on value) list of (country code, country name)-pairs. Since the order is based on
    value, these values must be translated on sorting. Ensure that you are calling this method in the proper i18n
    context!

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

    return tuple(sorted(((k, v) for k, v in ISO_3166_COUNTRIES.items() if k in countries and k not in exclude),
                        key=lambda item: item[1]))

get_countries_lazy = lazy(get_countries, six.string_types)