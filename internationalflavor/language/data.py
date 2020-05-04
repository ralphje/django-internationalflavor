from django.conf import settings
from django.utils.functional import lazy

from ._cldr_data import LANGUAGE_NAMES


def get_languages(languages=None, exclude=None):
    """Returns a list of (language code, language name)-pairs.

    Only languages present in the languages argument, and not present in the excluded argument, are returned. If you
    wish, for instance, to list all available languages, you could use get_languages(LANGUAGE_NAMES)
    """
    languages = settings.LANGUAGES if languages is None else languages
    exclude = exclude if exclude else []

    return [(k.lower(), v) for k, v in LANGUAGE_NAMES.items() if k.lower() in languages and k.lower() not in exclude]


get_languages_lazy = lazy(get_languages, list)

LANG_MIN_LENGTH = 2
LANG_MAX_LENGTH = 17
