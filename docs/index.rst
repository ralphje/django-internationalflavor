==========================
django-internationalflavor
==========================

:mod:`django-internationalflavor` is born to complement the :mod:`django-localflavor` package. While localflavor is
awesome when you are making a localized app, the reality is that you often need to accommodate for users from multiple
countries. While Django has great support for internationalization and localization, there is no package that helps you
store data from all over the world. This package aims to fill the gap and provides fields that are designed for use in
almost every country, while enforcing consistent data types.

.. warning::

   This module is far from complete and may or may not break your existing installation. I'm still working on it, so
   please bear with me. Pull requests are welcome!

Available data types
====================
.. toctree::
   :maxdepth: 1

   countries
   iban
   language
   names
   timezone
   vat_number
   changelog

(Expected soon: telephone numbers)

Basic principles
================
All validators enforce one specific format and generally do not allow any additional white-spacing, dashes or other
readability marks. These should not be present in your database, as readability is not a property of your data.
However, the provided model and form fields will strip these characters out and allow for a more seamless experience
for your users.

Most validators rely on data present in this module, but such data is likely to change over time. Trying to keep this
module up-to-date is one of the primary aims of this project, but from time to time an update may be missed. Please
send your pull requests for such oversights, preferably including a link to an official resource confirming the change.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`