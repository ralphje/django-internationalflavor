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

    # Fix issue #49
    cwp = os.path.dirname(os.path.abspath(__name__))
    pythonpath = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    pythonpath.append(os.path.join(cwp, 'tests'))
    os.environ['PYTHONPATH'] = os.pathsep.join(pythonpath)

    run('{0} internationalflavor'.format(flake_cmd))
    run('{0} tests'.format(test_cmd))
    run('coverage report')

# Taken from django-internationalflavor, but needs work
#@task
#def translations(pull=False, locale=None):
#    if pull:
#        if locale:
#            run('tx pull -l {0}'.format(locale))
#        else:
#            run('tx pull -a')
#    if locale:
#        run('cd localflavor; django-admin.py makemessages -l {0}; '
#            'django-admin.py compilemessages -l {0}; cd ..'.format(locale))
#    else:
#        run('cd localflavor; django-admin.py makemessages -a; '
#            'django-admin.py compilemessages; cd ..')


@task
def docs():
    run('cd docs; make html; cd ..')