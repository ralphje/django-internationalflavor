=========
Countries
=========
.. module:: internationalflavor.countries

Although for the most countries, sovereignty is not disputed, there are numerous cases where the definition of
country is not clear. Using the full ISO 3166-1 country list may seem the most political correct method, but this would
also include uninhabited wasteland such as Antartica and Norfolk Island. Furthermore, some territories are more or less
part of another country, such as Greenland that is part of Denmark.

To accommodate for these differences, this module chooses to include the following countries by default:

- All UN member states
- All UN disputed states (except for when no ISO 3166-1 country code is available)
- All UN observer states
- All UN non-self-governing states (this list is rather arbitrary, unfortunately)

Both fields provided by this module provide ways to manually add or exclude items from this list, as long as they are
valid ISO 3166-1 alpha-2 codes.

The list of ISO 3166-1 countries included with this module uses the common names of countries, rather than using their
official names.

.. note::

   While this module tries to provide some sort of equal ground most people would agree on, the choices that have been
   made may be grounds for disputes on sovereignty. First of all, I'm sorry if the choices that have been made make you
   feel uncomfortable. Second of all, you are not required to use the provided default list and you can easily include
   or exclude countries to your liking. And finally, you are welcome to open a ticket (or pull request) on Github, but
   please keep it civilized and try to maintain a unbiased position.

.. autoclass:: internationalflavor.countries.models.CountryField
.. autoclass:: internationalflavor.countries.forms.CountryFormField

Data constants
==============
You can use the following constants to specify your own set of available countries.

.. autodata:: internationalflavor.countries.data.UN_MEMBER_STATES
   :annotation: = (...)

.. autodata:: internationalflavor.countries.data.UN_OBSERVER_STATES
   :annotation: = (...)

.. autodata:: internationalflavor.countries.data.UN_DISPUTED_STATES
   :annotation: = (...)

.. autodata:: internationalflavor.countries.data.UN_NON_SELF_GOVERNING_STATES
   :annotation: = (...)

.. autodata:: internationalflavor.countries.data.UN_RECOGNIZED_COUNTRIES
   :annotation: = (...)

.. autodata:: internationalflavor.countries.data.IOC_RECOGNIZED_COUNTRIES
   :annotation: = (...)

Comparison with other packages
==============================
:mod:`django-countries`
   This module has a more elaborate ``CountryField``. It returns ``Country`` objects instead of ISO 3166-1 alpha-2 codes
   that allow easy access to the full name of a country or its country flag. However, it only provides the basic ISO
   country code list, with official country names (rather than using their common names).


.. seealso::
   `UN member states <http://www.un.org/en/members/index.shtml>`_
      List of UN member states.
   `UN observer states <http://www.un.org/en/members/nonmembers.shtml>`_
      List of UN observer states
   `UN non-self-governing states <http://www.un.org/en/decolonization/nonselfgovterritories.shtml>`_
      List of UN non-self-governing states
   `Wikpedia: List of ISO 3166-1 alpha-2 codes <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Current_codes>`_
      List of all ISO 3166-1 alpha-2 codes.
   `Wikipedia: List of sovereign states <https://en.wikipedia.org/wiki/List_of_sovereign_states#List_of_states>`_
      List of disputed sovereign states.
   `Wikipedia: Comparison of IOC ... country codes <https://en.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes>`_
      List of countries as recognized by the IOC.
