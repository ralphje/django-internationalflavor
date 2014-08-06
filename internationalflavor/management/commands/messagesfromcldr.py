import json
import os
from django.utils import translation
import polib
import tempfile
import zipfile
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import shutil
from internationalflavor.countries.data import ISO_3166_COUNTRIES

# We need a reverse lookup of ISO countries to get the translation strings
COUNTRY_LIST = dict(zip(ISO_3166_COUNTRIES.values(), ISO_3166_COUNTRIES.keys()))

class Command(BaseCommand):
    help = ('Updates locales of the internationalflavor module using data from the Unicode '
            'Common Locale Data Repository (CLDR)')
    args = '<path to cldr json zip>'

    def handle(self, *args, **options):
        # We need one argument
        if len(args) == 0:
            raise CommandError("You need to pass in a path to a zip containing CLDR JSON files.")
            
        # Ensure that we use the raw language strings, as we are going to modify the po files based on the
        # raw language strings.
        translation.deactivate_all()

        # Get the path to the locale directory
        path_to_locale = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'locale')
        
        try:
            # Unzip the files
            self.stdout.write("Reading CLDR from %s" % os.path.abspath(args[0]))
            
            with zipfile.ZipFile(args[0]) as cldr_zip:
                # Loop over all languages accepted by Django
                for lc, language in settings.LANGUAGES:
                    try:
                        self.stdout.write("Parsing language %s" % language)
                        
                        # Open the PO file
                        pofile = polib.pofile(os.path.join(path_to_locale, lc, 'LC_MESSAGES', 'django.po'))
    
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
                            # Update the territory information
                            if entry.msgid in COUNTRY_LIST and COUNTRY_LIST[entry.msgid] in territories and \
                                    territories[COUNTRY_LIST[entry.msgid]] != COUNTRY_LIST[entry.msgid] and \
                                    not 'manual' in entry.comment:
                                entry.msgstr = territories[COUNTRY_LIST[entry.msgid]]
                                entry.comment = "auto-generated from CLDR -- see docs before updating"
    
                        pofile.save()
                        pofile.save_as_mofile(os.path.join(path_to_locale, lc, 'LC_MESSAGES', 'django.mo'))
    
                    except IOError as e:
                        self.stderr.write("Error while handling %s: %s (possibly no valid .po file)" % (language, e))
    
                    except Exception as e:
                        self.stderr.write("Error while handling %s: %s" % (language, e))

        except OSError as e:
            raise CommandError("Error while reading zip file: %s" % e)
