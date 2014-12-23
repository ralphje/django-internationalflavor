from __future__ import absolute_import
from django.utils.functional import lazy
import itertools
from ._cldr_data import TIMEZONE_NAMES
from internationalflavor._helpers import orig_str


try:
    from pytz import common_timezones as COMMON_TIMEZONES
except ImportError:
    COMMON_TIMEZONES = [x for x in TIMEZONE_NAMES if not x.startswith("Etc")]


def get_timezones_cities(timezones=COMMON_TIMEZONES, exclude=()):
    """Returns a list of choices with (timezone code, exemplar city)-pairs, grouped by their territory.

    Only timezones present in the timezones argument, and not present in the excluded argument, are returned.
    """
    # We require sorting for the groupby
    values = sorted(TIMEZONE_NAMES.items(), key=lambda item: orig_str(item[1][0]))
    result = []
    for territory, zones in itertools.groupby(values, lambda item: item[1][0]):
        items = [(k, v[1]) for k, v in zones if k in timezones and k not in exclude]
        if items:
            result.append((territory, items))
    return result

get_timezones_cities_lazy = lazy(get_timezones_cities, list)
