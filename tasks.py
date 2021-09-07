from __future__ import print_function
import os
import os.path
import sys
from invoke import run, task


@task
def clean(ctx):
    run('git clean -Xfd')


@task
def test(ctx):
    print('Python version: ' + sys.version)
    # For some reason, the rcfile does not work properly under Py2.6 and Py2.7, so setting it explicitly here
    test_cmd = 'coverage run --source=internationalflavor --branch ' \
               '-m django test --settings=tests.settings'
    flake_cmd = 'flake8 --ignore=W801,E128,E501,W402,W503'

    cwp = os.path.dirname(os.path.abspath(__name__))
    pythonpath = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    pythonpath.append(os.path.join(cwp, 'tests'))
    os.environ['PYTHONPATH'] = os.pathsep.join(pythonpath)

    run('{0} internationalflavor'.format(flake_cmd))
    run('{0} tests'.format(test_cmd))
    run('coverage report')


@task
def compile_translations(ctx):
    run('python scripts/mergemessages.py')
    # run('cd internationalflavor; django-admin.py compilemessages; cd ..')


@task(post=[compile_translations])
def pull_translations(ctx, locale=None):
    if locale:
        run('tx pull -f -l {0}'.format(locale))
    else:
        run('tx pull --minimum-perc=1 -f -a')


@task(post=[compile_translations])
def make_translations(ctx, locale=None):
    if locale:
        run('cd internationalflavor; python -m django makemessages -l {0}; cd ..'.format(locale))
    else:
        run('cd internationalflavor; python -m django makemessages -a; cd ..')


@task(pre=[make_translations])
def push_translations(ctx):
    run('tx push -s')


@task(post=[make_translations])
def pull_cldr(ctx):
    if not os.path.exists("_cldr"):
        run('mkdir _cldr')
    run('cd _cldr; npm install cldr-localenames-full cldr-numbers-full cldr-dates-full cldr-core; cd ..')
    run('python scripts/datafromcldr.py _cldr/node_modules')


@task
def docs(ctx):
    run('cd docs; make html; cd ..')
