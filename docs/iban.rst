==========
IBAN / BIC
==========
.. module:: internationalflavor.iban

Most countries over the world use IBAN for international payments. Starting at August 1, 2014, the European Union has
mandated that all its member countries must use IBAN for domestic and international transactions. Even if your country
does not require IBAN for domestic transactions, it may be a good idea to use and store IBANs anyway. This allows you
to handle bank account numbers from different countries.

IBAN
====
.. autoclass:: internationalflavor.iban.validators.IBANValidator
.. autoclass:: internationalflavor.iban.models.IBANField
.. autoclass:: internationalflavor.iban.forms.IBANFormField

BIC
===
.. autoclass:: internationalflavor.iban.validators.BICValidator
.. autoclass:: internationalflavor.iban.models.BICField
.. autoclass:: internationalflavor.iban.forms.BICFormField


Comparison with other packages
==============================
:mod:`localflavor`
    Both an ``IBANField`` and a ``BICField`` are provided by this module. Although :mod:`internationalflavor` and
    :mod:`localflavor` have different approaches to validation, if you are already using :mod:`localflavor` and do
    not need any of the other fields provided by :mod:`internationalflavor`, you may be better off choosing
    :mod:`localflavor` (and vice versa).

:mod:`django-iban`
    The validation in this module is equal to the `localflavor` validation. The author of this package is seeking to
    retire his package, so it may be best to not use this package in new projects.

.. seealso::
   `IBAN Registry <https://www.swift.com/resource/iban-registry-pdf>`_
      The official IBAN format registry of SWIFT.
   `IBAN Structure <https://www.iban.com/structure>`_
      Additional IBAN formats listed as experimental
   `Wikipedia: International Bank Account Number <https://en.wikipedia.org/wiki/International_Bank_Account_Number>`_
      More information on IBAN