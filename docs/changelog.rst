=========
Changelog
=========

This file contains the changelog for the project.

0.2.0 (2015-02-09)
==================
* ``vat_number`` and ``iban``: Some consistency issues resolved; changed argument order and ``include_countries`` is now
  simply ``countries``.
* ``vat_number``: Do not imply ``eu_only`` when using ``vies_check``.
* ``vat_number``: Fallback to a native check if suds is not available.

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