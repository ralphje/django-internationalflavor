import datetime

from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _, ugettext
import itertools
from internationalflavor.timezone._cldr_data import TIMEZONE_NAMES, METAZONE_NAMES, METAZONE_MAPPING_FROM_TZ, \
    METAZONE_MAPPING_TO_TZ, TZ_REGION_FORMAT, TZ_GMT_FORMAT, TZ_HOUR_FORMAT
from internationalflavor._helpers import orig_str, string_format

from .._helpers import django_3_allowed

if django_3_allowed:
    from django.utils.translation import gettext_lazy as _

try:
    from pytz import common_timezones as COMMON_TIMEZONES
except ImportError:
    COMMON_TIMEZONES = [x for x in TIMEZONE_NAMES if not x.startswith("Etc")]


CURRENT_METAZONES = [x for x in set(METAZONE_MAPPING_FROM_TZ.values()) if x is not None]


def get_timezones_cities(timezones=None, exclude=None):
    """Returns a list of choices with (timezone code, exemplar city)-pairs, grouped by their territory.

    Only timezones present in the timezones argument, and not present in the exclude argument, are returned.
    """
    # We require sorting for the groupby
    timezones = COMMON_TIMEZONES if timezones is None else timezones
    exclude = exclude if exclude else []

    values = sorted(TIMEZONE_NAMES.items(), key=lambda item: orig_str(item[1][0]))
    result = []
    for territory, zones in itertools.groupby(values, lambda item: item[1][0]):
        items = [(k, v[1]) for k, v in zones if k in timezones and k not in exclude]
        if items:
            result.append((territory, items))
    return result


get_timezones_cities_lazy = lazy(get_timezones_cities, list)


def _get_metazone_cities(metazone, limit=5):
    zones = [tz for mz, tz in METAZONE_MAPPING_TO_TZ.items() if mz[0] == metazone]
    cities = sorted([territory[1] for tz, territory in TIMEZONE_NAMES.items() if tz in zones])

    if len(cities) > limit:
        return ", ".join(map(force_text, cities[:limit])) + ", ..."
    else:
        return ", ".join(map(force_text, cities))


_get_metazone_cities_lazy = lazy(_get_metazone_cities, str)


def _get_metazone_offset(metazone, correct_dst=True):
    try:
        import pytz
    except ImportError:
        raise ImproperlyConfigured("You can not use this display format without pytz")

    # We need to ensure that we do utcoffset - dst to get the normal offset for this timezone
    try:
        tzinfo = pytz.timezone(get_timezone_by_metazone(metazone))
        offset = tzinfo.utcoffset(datetime.datetime.now(), is_dst=False)
        if correct_dst:
            offset -= tzinfo.dst(datetime.datetime.now(), is_dst=False)
    except pytz.UnknownTimeZoneError:
        offset = datetime.timedelta(0)
    return offset


def _get_metazone_offset_str(metazone, correct_dst=True, include_gmt=True):
    offset = _get_metazone_offset(metazone, correct_dst=correct_dst)

    # Format the timezone
    if offset >= datetime.timedelta(0):
        offset_str = force_text(TZ_HOUR_FORMAT).split(';')[0]
    else:
        offset = -offset
        offset_str = force_text(TZ_HOUR_FORMAT).split(';')[1]
    offset_str = offset_str.replace('HH', "%02d" % (offset.total_seconds() // 3600))
    offset_str = offset_str.replace('mm', "%02d" % ((offset.total_seconds() % 3600) // 60))

    if include_gmt:
        return force_text(TZ_GMT_FORMAT) % offset_str
    else:
        return offset_str


_get_metazone_offset_str_lazy = lazy(_get_metazone_offset_str, str)


def get_metazone_name(metazone, display_format='name'):
    """Returns the name of a metazone, given a display_format. Available formats:

    *name* -- The name of the metazone, e.g.
                Central European Time
    *name_cities* -- The above two options combined, e.g.
                       Central European Time (Abidjan, Accra, Bamako, Banjul, Conakry, ...)
    *offset_name* -- The offset and the name, e.g.
                       GMT+01:00 Central European Time
    *offset_name_cities* -- The offset and the name, e.g.
                             GMT+01:00 Central European Time (Abidjan, Accra, Bamako, Banjul, Conakry, ...)

    Everything else is string formatted using traditional Python string formatting, with the following arguments
    available:

        * tzname
        * cities
        * offset
        * gmt_offset -- The offset including the GMT string
        * dst_offset -- The offset with current DST applied
        * gmt_dst_offset - The above two combined
    """
    if display_format == 'name':
        display_format = ugettext("%(tzname)s")
    elif display_format == 'name_cities':
        display_format = ugettext("%(tzname)s (%(cities)s)")
    elif display_format == 'offset_name':
        display_format = ugettext("%(gmt_offset)s %(tzname)s")
    elif display_format == 'offset_name_cities':
        display_format = ugettext("%(gmt_offset)s %(tzname)s (%(cities)s)")

    name = force_text(METAZONE_NAMES.get(metazone, string_format(TZ_REGION_FORMAT, _(metazone))))

    result = display_format % {
        'tzname': name,
        'cities': _get_metazone_cities_lazy(metazone),
        'offset': _get_metazone_offset_str_lazy(metazone, True, False),
        'gmt_offset': _get_metazone_offset_str_lazy(metazone, True, True),
        'dst_offset': _get_metazone_offset_str_lazy(metazone, False, False),
        'gmt_dst_offset': _get_metazone_offset_str_lazy(metazone, False, True)
    }

    return result


get_metazone_name_lazy = lazy(get_metazone_name, str)


def get_metazones(metazones=None, exclude=None, display_format='name'):
    """Returns a list of metazones.

    By default, returns all current metazones. If the metazones argument defines metazones, they are returned. Values
    in exclude are never returned.
    """
    metazones = CURRENT_METAZONES if metazones is None else metazones
    exclude = exclude if exclude else []

    return [(k, get_metazone_name_lazy(k, display_format)) for k in metazones if k not in exclude]


get_metazones_lazy = lazy(get_metazones, list)


def get_timezone_by_metazone(metazone, territories=None, fallback='001'):
    """Returns the timezone name from the metazone name. It takes three arguments:

    :param metazone: Name of the metazone
    :param territories: String of a single territory or a list of territories in order of preference for retrieving
                        the correct timezone. This is used when a metazone has multiple base timezones. It is optional
                        as there is always a fallback to the default 'World' territory (001). Use case: you could use
                        it to fill in the country of the user.
    :param fallback: The territory to use when no other territory could be found. This should always be 001 (=world)
    """

    if territories is None:
        territories = []
    elif isinstance(territories, str):
        territories = [territories]

    for ter in territories:
        if (metazone, ter) in METAZONE_MAPPING_TO_TZ:
            return METAZONE_MAPPING_TO_TZ[(metazone, ter)]
    return METAZONE_MAPPING_TO_TZ[(metazone, fallback)]
