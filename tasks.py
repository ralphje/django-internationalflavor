from __future__ import print_function
import os
import os.path
import sys
from invoke import run, task


@task
def clean():
    run('git clean -Xfd')


@task
def test():
    print('Python version: ' + sys.version)
    # For some reason, the rcfile does not work properly under Py2.6 and Py2.7, so setting it explicitly here
    test_cmd = 'coverage run --source=internationalflavor --branch ' \
               '`which django-admin.py` test --settings=tests.settings'
    flake_cmd = 'flake8 --ignore=W801,E128,E501,W402'

    cwp = os.path.dirname(os.path.abspath(__name__))
    pythonpath = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    pythonpath.append(os.path.join(cwp, 'tests'))
    os.environ['PYTHONPATH'] = os.pathsep.join(pythonpath)

    run('{0} internationalflavor'.format(flake_cmd))
    run('{0} tests'.format(test_cmd))
    run('coverage report')


@task
def compile_translations():
    run('python scripts/mergemessages.py')
    # run('cd internationalflavor; django-admin.py compilemessages; cd ..')


@task(post=[compile_translations])
def pull_translations(locale=None):
    if locale:
        run('tx pull -f -l {0}'.format(locale))
    else:
        run('tx pull --minimum-perc=1 -f -a')


@task(post=[compile_translations])
def make_translations(locale=None):
    if locale:
        run('cd internationalflavor; django-admin.py makemessages -l {0}; cd ..'.format(locale))
    else:
        run('cd internationalflavor; django-admin.py makemessages -a; cd ..')


@task(pre=[make_translations])
def push_translations():
    run('tx push -s')


@task(post=[make_translations])
def pull_cldr(path):
    run('python scripts/datafromcldr.py {0}'.format(path))


@task
def docs():
    run('cd docs; make html; cd ..')