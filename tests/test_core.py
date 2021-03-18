# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.test import SimpleTestCase
from internationalflavor.forms import SortedSelect


class SortedSelectTest(SimpleTestCase):
    def test_simple_sorted_select(self):
        f = SortedSelect(choices=[(1, _("Unknown Region")), (2, "Abuh")])
        out = '''<select name="test">
        <option value="2">Abuh</option>
        <option value="1" selected="selected">Unknown Region</option>
        </select>'''
        self.assertHTMLEqual(out, f.render('test', '1'))

    def test_sorted_select_with_optgroups(self):
        f = SortedSelect(choices=[("B", (("a", _("Unknown Region")), (2, "Abuh"))), ("z", "A"), ("x", "C")])
        # Due to the way Django 1.11 collects its options, we can't interleave options between optgroups anymore
        # So this is a behavioral change
        out = '''<select name="test">
          <optgroup label="B">
          <option value="2">Abuh</option>
          <option value="a" selected="selected">Unknown Region</option>
          </optgroup>
          <option value="z">A</option>
          <option value="x">C</option>
          </select>'''
        self.assertHTMLEqual(out, f.render('test', 'a'))

    def test_sorting_of_unicode_strings(self):
        import locale
        current_locale = locale.getlocale(locale.LC_COLLATE)
        try:
            new_locale = locale.setlocale(locale.LC_COLLATE, '')
            if 'UTF-8' not in new_locale:
                self.skipTest("No proper sortable context found")

            if locale.strcoll("z", "ą") < 0:
                self.skipTest("Sortable context does not sort properly (using BSD?)")

            f = SortedSelect(choices=[("0", "a"), ("1", "ą"), ("2", "z")])
            out = '''<select name="test">
            <option value="0" selected="selected">a</option>
            <option value="1">ą</option>
            <option value="2">z</option>
            </select>'''
            self.assertHTMLEqual(out, f.render('test', '0'))
        finally:
            locale.setlocale(locale.LC_COLLATE, current_locale)
