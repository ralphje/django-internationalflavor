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

The model field uses a :class:`datetime.tzinfo` Python object as representation, unless `use_tzinfo` is set to
:const:`False`. If :mod:`pytz` is not available, setting `use_tzinfo` to :const:`False` is required, as it is not
possible to convert between timezone names and :class:`datetime.tzinfo` objects without it.

.. autoclass:: internationalflavor.timezone.models.TimezoneField
.. autoclass:: internationalflavor.timezone.forms.TimezoneFormField

.. seealso::
   `Django: Time zones <https://docs.djangoproject.com/en/dev/topics/i18n/timezones/>`_
      Django documentation on time zones