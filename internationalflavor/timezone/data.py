from __future__ import absolute_import
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import lazy
import itertools
from ._cldr_data import TIMEZONE_NAMES


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


def _format_tz_name(*strings):
    return ', '.join(force_text(s) for s in strings[::-1])
format_tz_name = lazy(_format_tz_name, six.text_type)


def get_timezones_cities(timezones=COMMON_TIMEZONES, exclude=()):
    """Same as get_timezones_cities_sorted, but does not sort or group the values."""

    return [(k, format_tz_name(*v)) for k, v in TIMEZONE_NAMES.items() if k in timezones and k not in exclude]


get_timezones_cities_sorted_lazy = lazy(get_timezones_cities_sorted, list)
get_timezones_cities_lazy = lazy(get_timezones_cities, list)
