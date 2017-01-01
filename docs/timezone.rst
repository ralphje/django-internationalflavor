==========
Time zones
==========
.. module:: internationalflavor.timezone

Time zone support was added in Django 1.4, allowing you to store and handle local dates and times. It is highly
recommended to store your time objects timezone-aware. Django handles this for you, but it does not provide a way for a
user to save their timezone. This module adds support for this.

This module highly recommends you install :mod:`pytz` along with it, but it is not required. By default, the module
uses the set of common timezones as reported by :attr:`pytz.common_timezones`. If this is not available, the set as
provided by the CLDR is used instead.

This module provides two different types to store your timezones. The :class:`models.TimezoneField` model field uses
the default timezone database and the default form field requests the user to select a timezone based on their location.
This is the recommended approach and most consistent with how timezones are stored internally. You are ensured that you
will always be in the same timezone, and when a location changes its timezone, it is automatically applied.

The other option is to use metazones. These are defined by CLDR and often span multiple cities, i.e. you don't pick the
city and let the system figure out which timezone you are in based on the location, but let the user pick a timezone.
This has the advantage that it is more intuitive for the user and results in a much shorter dropdown menu, but has the
obvious disadvantage that it does not update automatically when a timezone is changed. It is also unsuitable for
accurate historic dates.

The model field uses a :class:`datetime.tzinfo` Python object as representation, unless `use_tzinfo` is set to
:const:`False`. If :mod:`pytz` is not available, setting `use_tzinfo` to :const:`False` is required, as it is not
possible to convert between timezone names and :class:`datetime.tzinfo` objects without it.

.. autoclass:: internationalflavor.timezone.models.TimezoneField
.. autoclass:: internationalflavor.timezone.forms.TimezoneFormField
.. autoclass:: internationalflavor.timezone.models.MetazoneField
.. autoclass:: internationalflavor.timezone.forms.MetazoneFormField

.. seealso::
   `Django: Time zones <https://docs.djangoproject.com/en/dev/topics/i18n/timezones/>`_
      Django documentation on time zones