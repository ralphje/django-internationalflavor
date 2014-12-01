from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import UTC
from django.utils.translation import ugettext_lazy as _
from internationalflavor.timezone.data import COMMON_TIMEZONES, get_timezones_cities_lazy
from internationalflavor.timezone.forms import TimezoneFormField


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

    def __init__(self, timezones=None, exclude=(), use_tzinfo=True, *args, **kwargs):
        if timezones is None:
            timezones = COMMON_TIMEZONES

        self.timezones = timezones
        self.exclude = exclude
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
            return UTC()
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
            value.tzname(None)
        else:
            return value