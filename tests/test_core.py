# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.test import SimpleTestCase
from internationalflavor.forms import SortedSelect


class SortedSelectTest(SimpleTestCase):
    def test_simple_sorted_select(self):
        f = SortedSelect()
        out = '''<select name="test">
        <option value="2">Abuh</option>
        <option value="1" selected="selected">Unknown Region</option>
        </select>'''
        self.assertHTMLEqual(f.render('test', '1', None, [(1, _("Unknown Region")), (2, "Abuh")]), out)

    def test_sorted_select_with_optgroups(self):
        f = SortedSelect()
        out = '''<select name="test">
        <option value="z">A</option>
        <optgroup label="B">
        <option value="2">Abuh</option>
        <option value="a" selected="selected">Unknown Region</option>
        </optgroup>
        <option value="x">C</option>
        </select>'''
        self.assertHTMLEqual(f.render('test', 'a', None, [("B", (("a", _("Unknown Region")), (2, "Abuh"))),
                                                          ("z", "A"), ("x", "C")]), out)

    def test_sorting_of_unicode_strings(self):
        import locale
        current_locale = locale.getlocale(locale.LC_COLLATE)
        try:
            new_locale = locale.setlocale(locale.LC_COLLATE, '')
            if 'UTF-8' not in new_locale:
                self.skipTest("No proper sortable context found")
            f = SortedSelect()
            out = '''<select name="test">
            <option value="0" selected="selected">a</option>
            <option value="1">ą</option>
            <option value="2">z</option>
            </select>'''
            self.assertHTMLEqual(f.render('test', '0', None, [("0", "a"), ("1", "ą"), ("2", "z")]), out)
        finally:
            locale.setlocale(locale.LC_COLLATE, current_locale)