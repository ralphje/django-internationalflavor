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


class Command(BaseCommand):
    help = 'Updates locales based on the Unicode CLDR'
    args = '<path to cldr zip>'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("You need to pass in a path to a zip containing CLDR JSON files.")
        translation.deactivate_all()  # ensure that we use the raw language strings

        # We need a reverse lookup of ISO countries to get the translation strings
        country_list = dict(zip(ISO_3166_COUNTRIES.values(), ISO_3166_COUNTRIES.keys()))

        path_to_locale = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'locale')
        unzipdir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(args[0]) as zf:
                self.stdout.write("Reading CLDR from %s" % os.path.abspath(args[0]))
                zf.extractall(unzipdir)

            for lc, language in settings.LANGUAGES:
                pofile = None
                try:
                    pofile = polib.pofile(os.path.join(path_to_locale, lc, 'LC_MESSAGES', 'django.po'))

                    if lc == 'zh-cn':
                        lc = 'zh-Hans-CN'
                    elif lc == 'zh-tw':
                        lc = 'zh-Hant-TW'
                    else:
                        lc = lc[0:3] + lc[3:].upper().replace("LATN", "Latn")

                    self.stdout.write("Parsing language %s" % language)
                    os.chdir(os.path.join(unzipdir, "main", lc))

                    with open("territories.json", "r") as f:
                        data = json.load(f)
                        territories = data['main'][lc]['localeDisplayNames']['territories']

                    for entry in pofile:
                        if entry.msgid in country_list and country_list[entry.msgid] in territories and \
                                not 'manual' in entry.comment:
                            entry.msgstr = territories[country_list[entry.msgid]]
                            entry.comment = "auto-generated from CLDR"

                    pofile.save()

                except IOError as e:
                    self.stderr.write("Error while handling %s: %s (possibly no valid .po file)" % (language, e))

                except Exception as e:
                    self.stderr.write("Error while handling %s: %s" % (language, e))

        except OSError as e:
            raise CommandError("Error while handling zip file: %s" % e)

        finally:
            self.stdout.write("Cleaning up...")
            shutil.rmtree(unzipdir)