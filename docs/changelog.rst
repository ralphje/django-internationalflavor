=========
Changelog
=========

This file contains the changelog for the project.

Future release
==============
* ``vat_number`` and ``iban``: Some consistency issues resolved; changed argument order and ``include_countries`` is now
  simply ``countries``.
* ``vat_number``: Do not imply ``eu_only`` when using ``vies_check``.

0.1.2 (2014-12-18)
==================
* Important packaging fixes

0.1.1 (2014-12-08)
==================
* ``iban``: Added support for IBANs from Kosovo and Timor-Leste, and Nordea extensions from Republic of Congo, Egypt and Gabon.

0.1 (2014-12-01)
================
* Initial release
* Added modules ``countries``, ``iban``, ``timezone`` and ``vat_number``