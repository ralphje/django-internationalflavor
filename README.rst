django-internationalflavor
==========================

:mod:`django-internationalflavor` is born to complement the :mod:`django-localflavor` package. While localflavor is
awesome when you are making a localized app, the reality is that you often need to accommodate for users from multiple
countries. While Django has great support for internationalization and localization, there is no package that helps you
store data from all over the world. This package aims to fill the gap and provides fields that are designed for use in
almost every country, while enforcing consistent data types.

Documentation
-------------
The documentation of this project is available at http://django-internationalflavor.readthedocs.org/en/latest/

The source code lives at https://github.com/ralphje/django-internationalflavor

Installation
------------

    pip install django-internationalflavor


Tests
-----
There are no tests yet. Sorry!

CLDR
----
The folder ``_scripts`` contains some useful scripts to update the repository data according to the CLDR. To update
all data, use::

    _scripts/datafromcldr.py cldr.zip

This will generate (or update) two types of files: all ``_cldr_data.py`` files, with dicts containing translatable
strings, and ``cldr.po`` files, that contain the translations of all CLDR strings. You can merge these into the
Django translation files using::

    _scripts/mergemessages.py

This command will also synchronize with file named ``django_only.po``, which can be used by translators to translate
messages (instead of the huge ``django.po`` file that also contains CLDR strings).

Translators should note that all CLDR data will be automatically overwritten with translations.