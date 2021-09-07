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

We use GitHub to keep track of issues and pull requests. You can always
`submit an issue <https://github.com/ralphje/django-internationalflavor/issues>`_ when you encounter something out of
the ordinary.

Development
===========
For some of the management commands below, we use ``invoke``, amongst other tools. To set up your development
environment, you probably want to install the requirements in the ``tests/requirements.txt`` file::

    $ git clone https://github.com/ralphje/django-internationalflavor
    $ virtualenv venvs/django-internationalflavor
    $ . venvs/django-internationalflavor/bin/activate
    $ cd django-internationalflavor
    $ pip install -r tests/requirements.txt

The documentation is built using Spinx. Additional requirements to build the documentation can be found in
``docs/requirements.txt``

Tests
=====
We use Tox to test this project in different environments. Running tests is therefore as simple as
`installing Tox <http://tox.readthedocs.org/en/latest/install.html>`_ and running it in the root checkout directory::

    $ git clone https://github.com/ralphje/django-internationalflavor
    $ cd django-internationalflavor
    $ tox
    [...]
      congratulations :)

If you only want to test in a specific environment, you can do so by using::

    tox -e py34-1.7

You can list all available environments with ``tox -l``.

Common Locale Data Repository
=============================
We use the CLDR for several pieces of international data. The following command can be ran to update the repository
data with the latest CLDR (requires npm as it uses this to pull the data off GitHub)::

    apt install gettext
    invoke pull-cldr

This will generate (or update) two types of files: all ``_cldr_data.py`` files, with dicts containing translatable
strings, and ``cldr.po`` files, that contain the translations of all CLDR strings.

Translations
============
If you wish to contribute translations, please do so
`online at Transifex <https://www.transifex.com/projects/p/django-internationalflavor/>`_.

If some translations from the CLDR are incorrect or incomplete, please contribute these online to
`the CLDR repository <http://cldr.unicode.org/index/survey-tool>`_.

Since we use the CLDR as an additional source of translations, we need to merge different files together. Instead of
running ``django-admin.py makemessages`` and ``django-admin.py compilemessages`` after changing any translation
strings, you should run::

    invoke make-translations

This will automatically find the translation strings (just as ``makemessages`` would), but additionally merges and
compiles the correct files. This should result in the following files in the repository:

* ``django.po`` and ``django.mo``, fully merged and compiled translation file which will be used by Django;
* ``django_only.po``, file solely containing the strings that are not translated by the CLDR - this file is kept in
  sync with Transifex. Newly discovered strings are automatically added in the same way as ``makemessages`` updates the
  ``django.po`` file;
* and ``cldr.po``, which is already created by ``pull_cldr``

Modifications in the ``django.po`` file will be lost when ``make_translations`` is ran: translated strings in
``django_only.po`` and ``cldr.po`` take precedence. Also note that the ``cldr.po`` file is automatically overwritten
when running ``pull_cldr``.

Transifex sync
--------------
This section only applies to those having maintainer access to the Transifex repository.

For these commands you need the Transifex client on your system, see
https://docs.transifex.com/client/installing-the-client

You can synchronize the translations with Transifex by running::

    invoke pull-translations

After new translations have been added, please run::

    invoke push-translations
