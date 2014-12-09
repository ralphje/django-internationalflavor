"""List of all VAT number regexes to be used for validating European VAT numbers. Regexes do not include any
formatting characters.

Sources:
EU: http://www.hmrc.gov.uk/vat/managing/international/esl/country-codes.htm
CA: http://www.cra-arc.gc.ca/tx/bsnss/tpcs/bn-ne/wrks-eng.html
others: https://en.wikipedia.org/wiki/VAT_identification_number
"""
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
    'HU': r'^[0-8]{8}$',
    'IE': r'^\d[A-Za-z0-9]\d{5}[A-Za-z]$',
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

    # Others
    # if no source listed above, these regexes are based on Wikipedia
    # patches (with sources) for these are welcome
    'AL': r'^[JK]\d{8}[A-Z]$',
    'AU': r'^\d{9}$',
    'BY': r'^\d{9}$',
    'CA': r'^\d{9}R[TPCMRDENGZ]\d{4}$',
    'IN': r'^\d{11}[CV]$',
    'NO': r'^\d{9}$',
    'PH': r'^\d{12}$',
    'RU': r'^(\d{10}|\d{12})$',
    'SM': r'^\d{5}$',
    'RS': r'^\d{9}$',
    'CH': r'^\d{9}$',
    'TR': r'^\d{10}$',
    'AR': r'^\d{11}$',
    # BO
    'BR': r'^\d{14}$',
    'CL': r'^\d{9}$',
    'CO': r'^\d{10}$',
    'CR': r'^\d{9,12}$',
    'EC': r'^\d{13}$',
    # SV
    'GT': r'^\d{8}$',
    # HN
    'MX': r'^[A-Z0-9]{3,4}\d{6}[A-Z0-9]{3}$',
    # NI, PA, PY
    'PE': r'^\d{11}$',
    # DO, UY
    'VE': r'^[EGJV]\d{9}$',

}

EU_VAT_AREA = ['AT', 'BE', 'BG', 'CV', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'GB', 'HR',
               'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'RO', 'SE', 'SI', 'SK']


VAT_MIN_LENGTH = 4   # Romania seems to have the shortest
VAT_MAX_LENGTH = 16  # BR seems to be the longest
