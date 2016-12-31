=========
Changelog
=========

This file contains the changelog for the project.

0.3.1 (unreleased)
==================
* Fix Django 1.11 bug in the SortedSelect widget. This affects the sorting of optgroups for all versions, they are now
  always sorted above other choices.
* Updated CLDR data from v29 to v30.0.3
* ``vat_number``: Additional cleanup for CH VAT numbers and validation for RU VAT numbers

0.3.0 (2016-08-20)
==================
* Fixes a Django 1.10 bug (I fixed it before, but it never made it into a release...)
* Updated CLDR and IBAN data. Note: UA got an official IBAN, so this means the Nordea alternative got dropped
  (SC also got a IBAN, but it was never in the Nordea set).

0.2.1 (2015-02-09)
==================
* Fixes a Python 3 bug discovered when releasing 0.2.0

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