===========
VAT numbers
===========
.. module:: internationalflavor.vat_number

VAT numbers are used in many countries for taxing purposes. In the European Union, organizations are required to use
these VAT numbers when conducting intra-Community trade and e.g. for reverse charging. Although there's no US equivalent
of a VAT number, these are used in most other countries around the world.

.. autoclass:: internationalflavor.vat_number.validators.VATNumberValidator
.. autoclass:: internationalflavor.vat_number.models.VATNumberField
.. autoclass:: internationalflavor.vat_number.forms.VATNumberFormField
