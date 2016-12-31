# coding=utf-8
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation

from internationalflavor.countries import CountryField
from internationalflavor.countries import CountryFormField


class CountriesFormTestCase(SimpleTestCase):
    def test_form_field(self):
        field = CountryFormField(countries=['NL', 'BE', 'FR'])
        self.assertEqual(set([f[0] for f in field.choices]), set(['BE', 'FR', 'NL']))

    def test_form_field_render(self):
        field = CountryFormField(countries=['NL', 'CF'])
        out = '''<select name="countries">
            <option value="CF">Central African Republic</option>
            <option value="NL" selected="selected">Netherlands</option>
            </select>'''

        self.assertHTMLEqual(field.widget.render('countries', 'NL'), out)

        with translation.override('de'):
            out = '''<select name="countries">
                <option value="NL" selected="selected">Niederlande</option>
                <option value="CF">Zentralafrikanische Republik</option>
                </select>'''

            self.assertHTMLEqual(field.widget.render('countries', 'NL'), out)

    def test_model_field_deconstruct_default(self):
        # test_instance must be created with the non-default options.
        test_inst = CountryField()
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = CountryField(*args, **kwargs)
        for attr in ('countries', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))

    def test_model_field_deconstruct_different(self):
        # test_instance must be created with the non-default options.
        test_inst = CountryField(countries=['NL', 'BE'], exclude=['BE'])
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = CountryField(*args, **kwargs)
        for attr in ('countries', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))
