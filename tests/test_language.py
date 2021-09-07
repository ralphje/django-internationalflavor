# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import SimpleTestCase, override_settings
from django.utils import translation

from internationalflavor.language.forms import LanguageFormField
from internationalflavor.language.models import LanguageField


class LanguageTestCase(SimpleTestCase):
    def test_form_field(self):
        field = LanguageFormField(languages=['nl', 'be'])
        self.assertEqual(set([f[0] for f in field.choices]), {'nl', 'be'})

    def test_form_field_render(self):
        field = LanguageFormField(languages=['nl', 'be'])
        out = '''<select name="languages">
            <option value="be">Belarusian</option>
            <option value="nl" selected="selected">Dutch</option>
            </select>'''

        self.assertHTMLEqual(field.widget.render('languages', 'nl'), out)

        with translation.override('de'):
            out = '''<select name="languages">
                <option value="be">Belarussisch</option>
                <option value="nl" selected="selected">Niederländisch</option>
                </select>'''

            self.assertHTMLEqual(field.widget.render('languages', 'nl'), out)

    @override_settings(LANGUAGES=['de', 'nl', 'it'])
    def test_model_languages_from_settings(self):
        field = LanguageField()
        self.assertEqual(set([f[0] for f in field.choices]), {'nl', 'de', 'it'})

    def test_capitalization(self):
        field = LanguageField(languages=['zh-hans', 'zh-hant', 'en-gb'])
        self.assertEqual(set([f[0] for f in field.choices]), {'en-gb', 'zh-hans', 'zh-hant'})

        out = '''<select name="languages">
            <option value="">---------</option>
            <option value="en-gb" selected="selected">British English</option>
            <option value="zh-hans">Simplified Chinese</option>
            <option value="zh-hant">Traditional Chinese</option>
            </select>'''

        self.assertHTMLEqual(field.formfield().widget.render('languages', 'en-gb'), out)

    def test_model_field_deconstruct_default(self):
        # test_instance must be created with the non-default options.
        test_inst = LanguageField()
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = LanguageField(*args, **kwargs)
        for attr in ('languages', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))

    def test_model_field_deconstruct_different(self):
        # test_instance must be created with the non-default options.
        test_inst = LanguageField(languages=['nl', 'be'], exclude=['be'])
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = LanguageField(*args, **kwargs)
        for attr in ('languages', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))
