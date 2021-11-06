import os
import re
import sys
import codecs
from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')


# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# Note: you may want to copy this into your setup.py file verbatim, as
# you can't import this from another package, when you don't know if
# that package is installed yet.
def find_package_data(where='.', package='',
                      exclude=standard_exclude,
                      exclude_directories=standard_exclude_directories,
                      only_in_packages=True,
                      show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.
    The dictionary looks like::
        {'package': [files]}
    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.
    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).
    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.
    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).
    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            sys.stderr.write("Directory %s ignored by pattern %s" % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py')) and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            sys.stderr.write("File %s ignored by pattern %s" % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


version = find_version("internationalflavor", "__init__.py")

try:
    long_description = open("README.rst", "r").read()
except Exception:
    long_description = None

setup(
    name='django-internationalflavor',
    version=version,
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data=find_package_data(),
    url='https://github.com/ralphje/django-internationalflavor',
    download_url='https://github.com/ralphje/django-internationalflavor/tarball/' + version,
    license='MIT',
    author='Ralph Broenink',
    author_email='ralph@ralphbroenink.net',
    description='Complementing django-localflavor with fields that are applicable to multiple countries',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
)
