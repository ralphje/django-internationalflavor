# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from django.utils.encoding import force_text

from internationalflavor.timezone.data import get_metazone_name, CURRENT_METAZONES
from internationalflavor.timezone.forms import TimezoneFormField, MetazoneFormField


class TimezoneTestCase(SimpleTestCase):
    def test_form_field(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/UTC'])
        self.assertEqual(set([force_text(f[0]) for f in field.choices]), set(['Europe', 'Americas', 'world']))
        self.assertEqual(set([force_text(g[0]) for f in field.choices for g in f[1]]),
                         set(['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/UTC']))

    def test_form_field_render(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/UTC', 'Indian/Christmas'])
        out = '''<select name="zones">
            <optgroup label="Americas">
            <option value="America/New_York">New York</option>
            </optgroup>
            <optgroup label="Europe">
            <option value="Europe/Amsterdam">Amsterdam</option>
            <option value="Europe/Berlin" selected="selected">Berlin</option>
            </optgroup>
            <optgroup label="world">
            <option value="Indian/Christmas">Christmas</option>
            <option value="Etc/UTC">UTC</option>
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
                <option value="Etc/UTC">UTC</option>
                <option value="Indian/Christmas">Weihnachtsinsel</option>
                </optgroup>
                </select>'''

            self.assertHTMLEqual(out, field.widget.render('zones', 'Europe/Berlin'))


class MetazoneTestCase(SimpleTestCase):
    def test_get_metazone_name(self):
        self.assertEqual(get_metazone_name('Europe_Central', 'name'),
                         'Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', 'name_cities'),
                         'Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name('Europe_Central', 'offset_name'),
                         'GMT+01:00 Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', 'offset_name_cities'),
                         'GMT+01:00 Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name('Europe_Central', '%(tzname)s'),
                         'Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', '%(cities)s'),
                         'Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...')
        self.assertEqual(get_metazone_name('Europe_Central', '%(gmt_offset)s'), 'GMT+01:00')
        self.assertEqual(get_metazone_name('Europe_Central', '%(offset)s'), '+01:00')
        with translation.override('bg'):
            self.assertEqual(get_metazone_name('Europe_Central', '%(gmt_offset)s'), 'Гринуич+01:00')

    def test_form_field(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'])
        self.assertEqual(set([force_text(f[0]) for f in field.choices]), set(['Europe_Central', 'GMT', 'Dushanbe']))

    def test_form_field_render_name(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'], display_format='name')
        out = '''<select name="zones">
            <option value="Europe_Central">Central European Time</option>
            <option value="Dushanbe" selected="selected">Dushanbe Time</option>
            <option value="GMT">Greenwich Mean Time</option>
            </select>'''
        self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))

        with translation.override('de'):
            out = '''<select name="zones">
            <option value="Dushanbe" selected="selected">Duschanbe Zeit</option>
            <option value="Europe_Central">Mitteleuropäische Zeit</option>
            <option value="GMT">Mittlere Greenwich-Zeit</option>
            </select>'''
            self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))

    def test_form_field_render_name_cities(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'], display_format='name_cities')
        out = '''<select name="zones">
            <option value="Europe_Central">Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)</option>
            <option value="Dushanbe" selected="selected">Dushanbe Time (Dushanbe)</option>
            <option value="GMT">Greenwich Mean Time (Abidjan, Accra, Bamako, Banjul, Conakry, ...)</option>
            </select>'''
        self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))
