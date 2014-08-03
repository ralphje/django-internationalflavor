"""Contains a list of all known IBAN regexes.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

"""Contains all country specific regexes for IBAN numbers.
Source: http://www.swift.com/dsp/resources/documents/IBAN_Registry.pdf
Accurate to version 49 (August 2014)
"""
IBAN_REGEXES = {
    'AD': r'^\d{10}[0-9A-Z]{12}$',  # AD2!n4!n4!n12!c
    'AE': r'^\d{21}$',  # AE2!n3!n16!n
    'AL': r'^\d{10}[0-9A-Z]{16}$',  # AL2!n8!n16!c
    'AT': r'^\d{18}$',  # AT2!n5!n11!n
    'AZ': r'^\d{2}[A-Z]{4}[0-9A-Z]{20}$',  # AZ2!n4!a20!c
    'BA': r'^\d{18}$',  # BA2!n3!n3!n8!n2!n
    'BE': r'^\d{14}$',  # BE2!n3!n7!n2!n
    'BG': r'^\d{2}[A-Z]{4}\d{6}[0-9A-Z]{8}$',  # BG2!n4!a4!n2!n8!c
    'BH': r'^\d{2}[A-Z]{4}[0-9A-Z]{14}$',  # BH2!n4!a14!c
    'BR': r'^\d{25}[A-Z][0-9A-Z]$',  # BR2!n8!n5!n10!n1!a1!c
    'CH': r'^\d{7}[0-9A-Z]{12}$',  # CH2!n5!n12!c
    'CR': r'r\d{19}$',  # CR2!n3!n14!n
    'CY': r'^\d{10}[0-9A-Z]{16}$',  # CY2!n3!n5!n16!c
    'CZ': r'^\d{22}$',  # CZ2!n4!n6!n10!n
    'DE': r'^\d{20}$',  # DE2!n8!n10!n
    'DK': r'^\d{16}$',  # DK2!n4!n9!n1!n
    'DO': r'^\d{2}[0-9A-Z]{4}\d{20}$',  # DO2!n4!c20!n
    'EE': r'^\d{18}$',  # EE2!n2!n2!n11!n1!n
    'ES': r'^\d{22}$',  # ES2!n4!n4!n1!n1!n10!n
    'FI': r'^\d{16}$',  # FI2!n6!n7!n1!n
    'FO': r'^\d{16}$',  # FO2!n4!n9!n1!n
    'FR': r'^\d{12}[0-9A-Z]{11}\d{2}$',  # FR2!n5!n5!n11!c2!n
    'GB': r'^\d{2}[A-Z]{4}\d{14}$',  # GB2!n4!a6!n8!n
    'GE': r'^\d{2}[A-Z]{2}\d{16}$',  # GE2!n2!a16!n
    'GI': r'^\d{2}[A-Z]{4}[0-9A-Z]{15}$',  # GI2!n4!a15!c:
    'GL': r'^\d{16}$',  # GL2!n4!n9!n1!n
    'GR': r'^\d{9}[0-9A-Z]{16}$',  # GR2!n3!n4!n16!c
    'GT': r'^\d{2}[0-9A-Z]{24}',  # GT2!n4!c20!c
    'HR': r'^\d{19}$',  # HR2!n7!n10!n
    'HU': r'^\d{26}$',  # HU2!n3!n4!n1!n15!n1!n
    'IE': r'^\d{2}[A-Z]{4}\d{14}$',  # IE2!n4!a6!n8!n
    'IL': r'^\d{21}$',  # IL2!n3!n3!n13!n
    'IS': r'^\d{24}$',  # IS2!n4!n2!n6!n10!n
    'IT': r'^\d{2}[A-Z]\d{10}[0-9A-Z]{12}$',  # IT2!n1!a5!n5!n12!c
    'JO': r'^\d{2}[A-Z]{4}\d{4}[0-9A-Z]{18}$',  # JO2!a2!n4!a4!n18!c
    'KW': r'^\d{2}[A-Z]{4}22!$',  # KW2!n4!a22!
    'KZ': r'^\d{5}[0-9A-Z]{13}$',  # KZ2!n3!n13!c
    'LB': r'^\d{6}[0-9A-Z]{20}$',  # LB2!n4!n20!c
    'LI': r'^\d{7}[0-9A-Z]{12}$',  # LI2!n5!n12!c
    'LT': r'^\d{18}$',  # LT2!n5!n11!n
    'LU': r'^\d{5}[0-9A-Z]{13}$',  # LU2!n3!n13!c
    'LV': r'^\d{2}[A-Z]{4}[0-9A-Z]{13}$',  # LV2!n4!a13!c
    'MC': r'^\d{12}[0-9A-Z]{11}\d{2}$',  # MC2!n5!n5!n11!c2!n
    'MD': r'^\d{2}[0-9A-Z]{20}$',  # MD2!n20!c
    'ME': r'^\d{20}$',  # ME2!n3!n13!n2!n
    'MK': r'^\d{5}[0-9A-Z]{10}\d{2}$',  # MK2!n3!n10!c2!n
    'MR': r'^\d{25}$',  # MR135!n5!n11!n2!n
    'MT': r'^\d{2}[A-Z]{4}\d{5}[0-9A-Z]{18}$',  # MT2!n4!a5!n18!c
    'MU': r'^\d{2}[A-Z]{4}\d{19}[A-Z]{3}$',  # MU2!n4!a2!n2!n12!n3!n3!a
    'NL': r'^\d{2}[A-Z]{4}\d{10}$',  # NL2!n4!a10!n
    'NO': r'^\d{13}$',  # NO2!n4!n6!n1!n
    'PK': r'^\d{2}[A-Z]{4}[0-9A-Z]{16}$',  # PK2!n4!a16!c
    'PL': r'^\d{10}[0-9A-Z]{,16}n',  # PL2!n8!n16n
    'PS': r'^\d{2}[A-Z]{4}[0-9A-Z]{21}$',  # PS2!n4!a21!c
    'PT': r'^\d{23}$',  # PT2!n4!n4!n11!n2!n
    'QA': r'^\d{2}[A-Z]{4}[0-9A-Z]{21}$',  # QA2!n4!a21!c
    'RO': r'^\d{2}[A-Z]{4}[0-9A-Z]{16}$',  # RO2!n4!a16!c
    'RS': r'^\d{20}$',  # RS2!n3!n13!n2!n
    'SA': r'^\d{4}[0-9A-Z]{18}$',  # SA2!n2!n18!c
    'SE': r'^\d{22}$',  # SE2!n3!n16!n1!n
    'SI': r'^\d{17}$',  # SI2!n5!n8!n2!n
    'SK': r'^\d{22}$',  # SK2!n4!n6!n10!n
    'SM': r'^\d{2}[A-Z]\d{10}[0-9A-Z]{12}$',  # SM2!n1!a5!n5!n12!c
    'TN': r'^\d{22}$',  # TN592!n3!n13!n2!n
    'TR': r'^\d{7}[0-9A-Z]{17}$',  # TR2!n5!n1!c16!c
    'VG': r'^\d{2}[A-Z]{4}\d{16}$',  # VG2!n4!a16!n
}

"""Nordea has some additional IBAN formats defined, which are not recognized by the SWIFT union.
https://www.nordea.com/Our+services/Cash+Management/Products+and+services/IBAN+countries/908462.html
"""
NORDEA_IBAN_REGEXES = {
    'AO': r'^\d{19}$',  # AOkk nnnn nnnn nnnn nnnn nnnn n
    'BF': r'^\d{25}$',   # BFkk nnnn nnnn nnnn nnnn nnnn nnn
    'BI': r'^\d{14}$',  # BIkk nnnn nnnn nnnn
    'BJ': r'^\d{2}[A-Z]\d{23}$',  # BJkk annn nnnn nnnn nnnn nnnn nnnn
    'CI': r'^\d{2}[A-Z]\d{23}$',  # CIkk annn nnnn nnnn nnnn nnnn nnnn
    'CM': r'^\d{25}$',  # CMkk nnnn nnnn nnnn nnnn nnnn nnn
    'CV': r'^\d{23}$',  # CVkk nnnn nnnn nnnn nnnn nnnn n
    'DZ': r'^\d{18}$',  # DZkk nnnn nnnn nnnn nnnn nnnn
    'IR': r'^\d{24}$',  # IRkk nnnn nnnn nnnn nnnn nnnn nn
    'MG': r'^\d{25}$',  # MGkk nnnn nnnn nnnn nnnn nnnn nnn
    'ML': r'^\d{2}[A-Z]\d{23}$',  # MLkk annn nnnn nnnn nnnn nnnn nnnn
    'MZ': r'^\d{23}$',  # MZkk nnnn nnnn nnnn nnnn nnnn n
    'SN': r'^\d{2}[A-Z]\d{23}$',  # SNkk annn nnnn nnnn nnnn nnnn nnnn
    'UA': r'^\d{2}[A-Z0-9]{6}\d{19}$',  # UAkk bbbb bbcc cccc cccc cccc cccc c
}


# FI includes AX for SEPA
# FR includes GF* GP* MQ* RE* PF TF YT* NC BL MF PM* WF (* incl for SEPA)
# PT includes Azores and Madeira for SEPA
"""List of all sepa country codes."""
SEPA_COUNTRIES = ['AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES',
                  'FI', 'FO', 'GB', 'GI', 'GL', 'GR', 'HU', 'IE', 'IS', 'IT',
                  'LI', 'LT', 'LU', 'LV', 'MC', 'MT', 'NL', 'NO', 'PL', 'PT',
                  'RO', 'SE', 'SI', 'SK']

IBAN_MIN_LENGTH = 16  # Belgium seems to have the shortest
IBAN_MAX_LENGTH = 34
