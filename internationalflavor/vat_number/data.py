VAT_NUMBER_REGEXES = {
    # EU VAT number regexes have a high certainty
    'AT': r'^U\d{8}$',
    'BE': r'^[01]\d{9}$',
    'BG': r'^\d{9,10}$',
    'CY': r'^\d{8}[A-Z]$',
    'CZ': r'^\d{8,10}$',
    'DE': r'^\d{9}$',
    'DK': r'^\d{8}$',
    'EE': r'^\d{9}$',
    'EL': r'^\d{9}$',
    'ES': r'^([A-Z]\d{7}[A-Z0-9]|\d{8}[A-Z])$',
    'FI': r'^\d{8}$',
    'FR': r'^[A-Z0-9]{2}\d{9}$',
    'GB': r'^(\d{9}|\d{12}|GD\d{3}|HA\d{3})$',
    'HR': r'^\d{11}$',
    'HU': r'^[0-9]{8}$',
    'IE': r'^(\d[A-Z0-9]\d{5}[A-Z]|\d{7}[A-Z]{2})$',
    'IT': r'^\d{11}$',
    'LT': r'^(\d{9}|\d{12})$',
    'LU': r'^\d{8}$',
    'LV': r'^\d{11}$',
    'MT': r'^\d{8}$',
    'NL': r'^\d{9}B\d{2}$',
    'PL': r'^\d{10}$',
    'PT': r'^\d{9}$',
    'RO': r'^\d{2,10}$',
    'SE': r'^\d{12}$',
    'SI': r'^\d{8}$',
    'SK': r'^\d{10}$',
    'XI': r'^(\d{9}|\d{12}|GD\d{3}|HA\d{3})$',
    'EU': r'^\d{9}$',

    # Others
    # if no source listed below, these regexes are based on Wikipedia
    # patches (with sources) for these are welcome
    'AL': r'^[JK]\d{8}[A-Z]$',
    'MK': r'^\d{13}$',
    'AU': r'^\d{9}$',
    'BY': r'^\d{9}$',
    'CA': r'^\d{9}R[TPCMRDENGZ]\d{4}$',
    'IS': r'^\d{5,6}$',
    'IN': r'^\d{11}[CV]$',
    'ID': r'^\d{15}$',
    'IL': r'^\d{9}$',
    'KZ': r'^\d{12}$',
    'NZ': r'^\d{9}$',
    'NG': r'^\d{12}$',
    'NO': r'^\d{9}$',
    'PH': r'^\d{12}$',
    'RU': r'^(\d{10}|\d{12})$',
    'SM': r'^\d{5}$',
    'RS': r'^\d{9}$',
    'CH': r'^[E]?\d{9}$',
    'TR': r'^\d{10}$',
    'UA': r'^\d{12}$',
    'UZ': r'^\d{9}$',

    'AR': r'^\d{11}$',
    'BO': r'^\d{7}$',
    'BR': r'^\d{14}$',
    'CL': r'^\d{9}$',
    'CO': r'^\d{10}$',
    'CR': r'^\d{9,12}$',
    'EC': r'^\d{13}$',
    'SV': r'^\d{14}$',
    'GT': r'^\d{8}$',
    # HN
    'MX': r'^[A-Z0-9]{3,4}\d{6}[A-Z0-9]{3}$',
    'NI': r'^\d{13}[A-Z]$',
    # PA
    'PY': r'^\d{7,9}$',
    'PE': r'^\d{11}$',
    'DO': r'^(\d{9}|\d{11})$',
    'UY': r'^\d{12}$',
    'VE': r'^[EGJV]\d{9}$',
}
"""List of all VAT number regexes to be used for validating European VAT numbers. Regexes do not include any
formatting characters.

Sources:
EU: http://www.hmrc.gov.uk/vat/managing/international/esl/country-codes.htm
CA: http://www.cra-arc.gc.ca/tx/bsnss/tpcs/bn-ne/wrks-eng.html
others: https://en.wikipedia.org/wiki/VAT_identification_number
"""

EU_VAT_AREA = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'XI', 'HR',
               'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

VAT_MIN_LENGTH = 4   # Romania seems to have the shortest
VAT_MAX_LENGTH = 16  # BR seems to be the longest
