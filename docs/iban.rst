====
IBAN
====
.. module:: internationalflavor.iban

Most countries over the world use IBAN for international payments. Starting at August 1, 2014, the European Union has
mandated that all its member countries must use IBAN for domestic and international transactions. Even if your country
does not require IBAN for domestic transactions, it may be a good idea to use and store IBANs anyway. This allows you
to handle bank account numbers from different countries.

Please note that :mod:`localflavor` also supports a ``IBANField``, but that module does not validate against regular
expressions, but rather validate the length of the IBAN. This means that the validation in this module is more
extensive. Additionally, this module contributes a ``BICField`` for SWIFT BIC validation.

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

.. seealso::
   `IBAN Registry <http://www.swift.com/dsp/resources/documents/IBAN_Registry.pdf>`_
      The official IBAN format registry of SWIFT.
   `Nordea IBAN countries <https://www.nordea.com/Our+services/Cash+Management/Products+and+services/IBAN+countries/908462.html>`_
      Additional IBAN formats as recognized by Nordea.
   `Wikipedia: International Bank Account Number <https://en.wikipedia.org/wiki/International_Bank_Account_Number>`_
      More information on IBAN