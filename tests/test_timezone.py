from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from django.utils.encoding import force_text
from internationalflavor.timezone.forms import TimezoneFormField


class CountriesTestCase(SimpleTestCase):
    def test_form_field(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT'])
        self.assertEqual(set([force_text(f[0]) for f in field.choices]), set(['Europe', 'Americas', 'World']))
        self.assertEqual(set([force_text(g[0]) for f in field.choices for g in f[1]]),
                         set(['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT']))

    def test_form_field_render(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT', 'Indian/Christmas'])
        out = '''<select name="zones">
            <optgroup label="Americas">
            <option value="America/New_York">New York</option>
            </optgroup>
            <optgroup label="Europe">
            <option value="Europe/Amsterdam">Amsterdam</option>
            <option value="Europe/Berlin" selected="selected">Berlin</option>
            </optgroup>
            <optgroup label="World">
            <option value="Indian/Christmas">Christmas</option>
            <option value="Etc/GMT">GMT</option>
            </optgroup>
            </select>'''
        self.assertHTMLEqual(out, field.widget.render('zones', 'Europe/Berlin'))

        with translation.override('de'):
            out = '''<select name="zones">
                <optgroup label="Amerika">
                <option value="America/New_York">New York</option>
                </optgroup>
                <optgroup label="Europa">
                <option value="Europe/Amsterdam">Amsterdam</option>
                <option value="Europe/Berlin" selected="selected">Berlin</option>
                </optgroup>
                <optgroup label="Welt">
                <option value="Etc/GMT">GMT</option>
                <option value="Indian/Christmas">Weihnachtsinsel</option>
                </optgroup>
                </select>'''

            self.assertHTMLEqual(out, field.widget.render('zones', 'Europe/Berlin'))