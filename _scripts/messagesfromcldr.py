import argparse
import json
import os
import zipfile

import polib
import django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation



# This is almost a management command, but we do not want it to be added to the django-admin namespace for the simple
# reason that it is not expected to be executed by package users, only by the package maintainers.
# We use a thin __main__ wrapper to make it work (ish) like a management command.


class Command(BaseCommand):
    help = ('Updates locales of the internationalflavor module using data from the Unicode '
            'Common Locale Data Repository (CLDR)')

    def handle(self, *args, **options):
        # Ensure that we use the raw language strings, as we are going to modify the po files based on the
        # raw language strings.
        translation.deactivate_all()

        # Prepare and load some constants (we can't do this earlier to ensure settings.configure has run)
        from internationalflavor.countries.data import COUNTRY_NAMES
        # Alternative entries in the CLDR list we use
        from _common import COUNTRY_ALTERNATIVE_KEYS
        # We need a reverse lookup of ISO countries to get the translation strings
        COUNTRY_LIST = dict(zip(COUNTRY_NAMES.values(), COUNTRY_NAMES.keys()))
        # Get the path to the locale directory
        PATH_TO_LOCALE = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'internationalflavor', 'locale')

        try:
            # Unzip the files
            self.stdout.write("Reading CLDR from %s" % os.path.abspath(options['path_to_cldr']))

            with zipfile.ZipFile(options['path_to_cldr']) as cldr_zip:
                # Loop over all languages accepted by Django
                for lc, language in settings.LANGUAGES:
                    try:
                        self.stdout.write("Parsing language %s" % language)

                        # Open the PO file
                        pofile = polib.pofile(os.path.join(PATH_TO_LOCALE, lc, 'LC_MESSAGES', 'django.po'))

                        # Rather ugly method to convert locale names, but it works properly for all accepted languages
                        if lc == 'zh-cn':
                            cldr_lc = 'zh-Hans-CN'
                        elif lc == 'zh-tw':
                            cldr_lc = 'zh-Hant-TW'
                        else:
                            cldr_lc = lc[0:3] + lc[3:].upper().replace("LATN", "Latn")

                        # Load territories data. Unsure whether this is according to CLDR recommendation, but it does
                        # not matter for this script. It is not exactly meant to be ran by end-users.
                        data = json.loads(cldr_zip.read(os.path.join("main", cldr_lc, "territories.json")).decode("utf8"))
                        territories = data['main'][cldr_lc]['localeDisplayNames']['territories']

                        for entry in pofile:
                            # Skip entries marked as manual
                            if 'manual' in entry.comment:
                                continue

                            # Update the territory information
                            if entry.msgid in COUNTRY_LIST:
                                territory = COUNTRY_LIST[entry.msgid]

                                # Use the short HK/MO/PS name if available
                                if territory in COUNTRY_ALTERNATIVE_KEYS and \
                                                COUNTRY_ALTERNATIVE_KEYS[territory] in territories and \
                                                territories[COUNTRY_ALTERNATIVE_KEYS[territory]] != territory:
                                    territory = COUNTRY_ALTERNATIVE_KEYS[territory]

                                # Only use the territory name if it exists and is not the country code itself
                                if territory in territories and territories[territory] != territory:
                                    entry.msgstr = territories[territory]
                                    entry.comment = "auto-generated from CLDR -- see docs before updating"

                        pofile.save()
                        pofile.save_as_mofile(os.path.join(PATH_TO_LOCALE, lc, 'LC_MESSAGES', 'django.mo'))

                    except IOError as e:
                        self.stderr.write("Error while handling %s: %s (possibly no valid .po file)" % (language, e))

                    except Exception as e:
                        self.stderr.write("Error while handling %s: %s" % (language, e))

        except OSError as e:
            raise CommandError("Error while reading zip file: %s" % e)


if __name__ == '__main__':
    settings.configure()
    if hasattr(django, 'setup'):
        django.setup()

    # We parse arguments ourselves. Django 1.8 uses argparse (finally) but we can just as easily use it ourselves.
    parser = argparse.ArgumentParser(description=Command.help)
    parser.add_argument('path_to_cldr', help='Path to a zip file containing CLDR JSON files.')
    args = parser.parse_args()

    Command().execute(**vars(args))