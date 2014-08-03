from distutils.core import setup

setup(
    name='django-internationalflavor',
    version='0.1',
    packages=['internationalflavor', 'internationalflavor.iban', 'internationalflavor.countries',
              'internationalflavor.vat_number'],
    url='https://github.com/ralphje/django-internationalflavor',
    license='MIT',
    author='Ralph Broenink',
    author_email='ralph@ralphbroenink.net',
    description='Complementing django-localflavor with fields that are applicable to multiple countries'
)
