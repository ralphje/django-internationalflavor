from django.utils.functional import lazy
import itertools
from _cldr_data import METAZONE_NAMES, TIMEZONE_NAMES, METAZONE_MAPPING


try:
    from pytz import common_timezones as COMMON_TIMEZONES
except ImportError:
    COMMON_TIMEZONES = [x for x in TIMEZONE_NAMES if not x.startswith("Etc")]


def get_timezones_cities_sorted(timezones=COMMON_TIMEZONES, exclude=()):
    """Returns a sorted list of (timezone code, exemplar city)-pairs, grouped by their territory. The order is based on
    the translated value, so these values must be translated on sorting. Ensure that you are calling this method in the
    proper i18n context!

    Only timezones present in the timezones argument, and not present in the excluded argument, are returned.
    """
    values = sorted(TIMEZONE_NAMES.items(), key=lambda item: item[1])
    result = []
    for territory, zones in itertools.groupby(values, lambda item: item[1][0]):
        result.append((territory, [(k, v[1]) for k, v in zones if k in timezones and k not in exclude]))
    return result


def get_timezones_cities(timezones=COMMON_TIMEZONES, exclude=()):
    """Same as get_timezones_cities_sorted, but does not sort or group the values."""

    return [(k, ', '.join(v[::-1])) for k, v in TIMEZONE_NAMES.items() if k in timezones and k not in exclude]


get_timezones_cities_sorted_lazy = lazy(get_timezones_cities_sorted, list)
get_timezones_cities_lazy = lazy(get_timezones_cities, list)