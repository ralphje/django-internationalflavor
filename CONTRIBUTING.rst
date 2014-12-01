==========================================
Contributing to django-internationalflavor
==========================================
Since django-internationalflavor is an open source project, contributions of many forms are welcomed. Examples of
possible contributions include:

* Bug patches
* Data corrections
* New features
* Documentation improvements
* Bug reports and reviews of pull requests

Tests
=====
Running tests is as simple as `installing Tox <http://tox.readthedocs.org/en/latest/install.html>`_ and running it in
the root directory.

Common Locale Data Repository
=============================
The folder ``scripts`` contains some useful scripts to update the repository data according to the CLDR. To update
all data, use::

    scripts/datafromcldr.py cldr.zip

This will generate (or update) two types of files: all ``_cldr_data.py`` files, with dicts containing translatable
strings, and ``cldr.po`` files, that contain the translations of all CLDR strings. You can merge these into the
Django translation files using::

    scripts/mergemessages.py

This command will also synchronize with a file named ``django_only.po``, which can be used by translators to translate
messages (instead of the huge ``django.po`` file that also contains CLDR strings).

The repository should only contain a compiled ``django.mo`` file, the ``cldr.po`` and ``django_only.po`` files don't
need to be compiled.

Always run ``mergemessages.py`` after running ``django-admin makemessages``.

Translators should note that all CLDR data will be automatically overwritten with translations. If any modification is
required, a translation should be made in the ``django.po`` file (as ``cldr.po`` is always overwritten) and marked
with a comment containing the text ``manual``. However, please submit corrected translations always to the CLDR.
