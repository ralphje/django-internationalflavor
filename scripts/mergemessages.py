import argparse
import os
import polib
import django
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation


# This is almost a management command, but we do not want it to be added to the django-admin namespace for the simple
# reason that it is not expected to be executed by package users, only by the package maintainers.
# We use a thin __main__ wrapper to make it work (ish) like a management command.

MODULE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'internationalflavor')
LOCALE_PATH = os.path.join(MODULE_PATH, 'locale')


def mark_entry(entry):
    if 'fuzzy' in entry.flags:
        entry.flags.remove('fuzzy')
    entry.comment = "auto-generated from CLDR -- see docs before updating"


class Command(BaseCommand):
    help = 'Updates messages in the PO file with messages from the CLDR'

    def handle(self, *args, **options):
        translation.deactivate_all()

        if options['l']:
            languages = (options['l'], dict(settings.LANGUAGES)[options['l']]),
        else:
            languages = settings.LANGUAGES

        for lc, language in languages:
            try:
                self.stdout.write("Parsing language %s [%s]" % (language, lc))

                # Get some files ready
                # The pofile is our combined file
                pofile = polib.pofile(os.path.join(LOCALE_PATH, lc, 'LC_MESSAGES', 'django.po'))
                # The cldrfile contain only messages from CLDR
                cldrfile = polib.pofile(os.path.join(LOCALE_PATH, lc, 'LC_MESSAGES', 'cldr.po'))
                # The djangofile will only contain messages not from CLDR
                try:
                    djangofile = polib.pofile(os.path.join(LOCALE_PATH, lc, 'LC_MESSAGES', 'django_only.po'))
                except IOError:
                    djangofile = polib.POFile()
                    djangofile.metadata = pofile.metadata
                    djangofile.header = pofile.header

                # Merge all non-django messages to the djangofile
                django_only_messages = polib.POFile()
                for entry in pofile:
                    if cldrfile.find(entry.msgid) is None and not entry.obsolete and not 'fuzzy' in entry.flags:
                        django_only_messages.append(entry)
                djangofile.merge(django_only_messages)
                djangofile.save(os.path.join(LOCALE_PATH, lc, 'LC_MESSAGES', 'django_only.po'))

                # Add all entries from the CLDR file to the combined file
                for entry in cldrfile:
                    e = pofile.find(entry.msgid)
                    if e is None:
                        e = polib.POEntry()
                        e.msgid = entry.msgid
                        pofile.append(e)
                    elif 'manual' in e.tcomment.lower():
                        self.stdout.write("-- Skipping %s of %s" % (e.msgid, language))
                        continue

                    e.obsolete = False
                    e.msgstr = entry.msgstr
                    e.comment = entry.comment
                    if 'fuzzy' in e.flags:
                        e.flags.remove('fuzzy')

                # Add entries from the Django file to the combined file
                for entry in djangofile:
                    e = pofile.find(entry.msgid)
                    # If not in main file, then skip
                    if e is None:
                        continue
                    e.obsolete = entry.obsolete
                    e.msgstr = entry.msgstr
                    e.comment = entry.comment
                    e.flags = entry.flags
                # We copy over the header and metadata from the djangofile.
                pofile.metadata = djangofile.metadata
                pofile.header = djangofile.header

                pofile.save()
                pofile.save_as_mofile(os.path.join(LOCALE_PATH, lc, 'LC_MESSAGES', 'django.mo'))

            except IOError as e:
                self.stderr.write("Error while handling %s: %s (possibly no valid .po file)" % (language, e))

            except Exception as e:
                self.stderr.write("Error while handling %s: %s" % (language, e))

if __name__ == '__main__':
    settings.configure()
    if hasattr(django, 'setup'):
        django.setup()

    # We parse arguments ourselves. Django 1.8 uses argparse (finally) but we can just as easily use it ourselves.
    parser = argparse.ArgumentParser(description=Command.help)
    parser.add_argument('-l')
    args = parser.parse_args()

    Command().execute(**vars(args))