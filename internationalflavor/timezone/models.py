from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from internationalflavor.timezone.data import COMMON_TIMEZONES, CURRENT_METAZONES, \
    METAZONE_MAPPING_FROM_TZ, get_timezones_cities_lazy, get_metazones_lazy, get_timezone_by_metazone
from internationalflavor.timezone.forms import TimezoneFormField, MetazoneFormField

try:
    import pytz
except ImportError:
    pytz = None


class TimezoneField(models.CharField):
    """A model field that allows users to choose their timezone. By default, all timezones in the set of common
    timezones of pytz are available. Use the ``timezones`` argument to specify your own timezones, and use ``exclude``
    to exclude specific zones.

    If ``use_tzinfo`` is :const:`True`, an instance of :class:`datetime.tzinfo` is returned. This requires :mod:`pytz`
    to be installed. If ``use_tzinfo`` is :const:`False`, a string is returned instead.
    """

    description = _('A timezone')

    def __init__(self, timezones=None, exclude=None, use_tzinfo=True, *args, **kwargs):
        if timezones is None:
            timezones = COMMON_TIMEZONES

        self.timezones = timezones
        self.exclude = exclude if exclude else []
        self.use_tzinfo = use_tzinfo

        kwargs.setdefault('max_length', 30)
        kwargs['choices'] = get_timezones_cities_lazy(timezones, exclude)

        super(TimezoneField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TimezoneField, self).deconstruct()
        if self.timezones != COMMON_TIMEZONES:
            kwargs['timezones'] = self.timezones
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if 'max_length' in kwargs and kwargs["max_length"] == 30:
            del kwargs["max_length"]
        del kwargs["choices"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': TimezoneFormField}
        defaults.update(kwargs)
        return super(TimezoneField, self).formfield(**defaults)

    def to_python(self, value):
        if not value:
            return None
        elif not self.use_tzinfo:
            return value
        elif isinstance(value, datetime.tzinfo):
            return value
        elif value in ('UTC', 'GMT'):
            return utc
        elif pytz is not None:
            try:
                return pytz.timezone(value)
            except pytz.UnknownTimeZoneError:
                pass
        raise ValidationError(_("Timezone %s is invalid") % value)

    def get_prep_value(self, value):
        if not value:
            return None
        elif hasattr(value, 'zone'):
            return value.zone
        elif hasattr(value, 'tzname'):
            return value.tzname(None)
        else:
            return value


class MetazoneField(models.CharField):
    """A model field that allows users to choose their metazone. By default, all metazones in the CLDR set are
    available. Use the ``metazones`` argument to specify your own metazones, and use ``exclude``
    to exclude specific zones.

    If ``use_tzinfo`` is :const:`True`, an instance of :class:`datetime.tzinfo` is returned. This requires :mod:`pytz`
    to be installed. Note, however, that only one exemplar timezone tzinfo is returned for the metazone. The exemplar
    timezone may change over time as cities change their timezones.

    If ``use_tzinfo`` is :const:`False`, a string is returned instead.
    """

    description = _('A metazone')

    def __init__(self, metazones=None, exclude=None, use_tzinfo=True, display_format='name', *args, **kwargs):
        if metazones is None:
            metazones = CURRENT_METAZONES

        self.metazones = metazones
        self.exclude = exclude if exclude else []
        self.use_tzinfo = use_tzinfo
        self.display_format = display_format

        kwargs.setdefault('max_length', 30)
        kwargs['choices'] = get_metazones_lazy(metazones, exclude, display_format=display_format)

        super(MetazoneField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MetazoneField, self).deconstruct()
        if self.metazones != CURRENT_METAZONES:
            kwargs['metazones'] = self.metazones
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if 'max_length' in kwargs and kwargs["max_length"] == 30:
            del kwargs["max_length"]
        del kwargs["choices"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': MetazoneFormField}
        defaults.update(kwargs)
        return super(MetazoneField, self).formfield(**defaults)

    def to_python(self, value):
        if not value:
            return None
        elif not self.use_tzinfo:
            return value
        elif isinstance(value, datetime.tzinfo):
            return value
        elif value in ('UTC', 'GMT'):  # GMT is also a metazone
            return utc
        elif pytz is not None:
            # Find a metazone with this name and return a city for this metazone
            try:
                return pytz.timezone(get_timezone_by_metazone(value))
            except pytz.UnknownTimeZoneError:
                pass
        raise ValidationError(_("Metazone %s is invalid") % value)

    def get_prep_value(self, value):
        if not value:
            return None
        elif hasattr(value, 'zone'):
            return METAZONE_MAPPING_FROM_TZ.get(value.zone, None)
        elif hasattr(value, 'tzname'):
            return METAZONE_MAPPING_FROM_TZ.get(value.tzname(None), None)
        else:
            return value
