import django
from django.utils.functional import lazy


def orig_str(lazy_str):
    return lazy_str._proxy____args[0]


def _string_format(str, format):
    """
    Lazy variant of string formatting, needed for situations where string
    formatting may be evaluated before it is calculated
    """
    return str % format


def _check_version(version):
    """ compare the current django version with the one passed in argument
    :returns: Boolean
    """
    from distutils.version import StrictVersion
    # https://docs.djangoproject.com/en/3.0/releases/3.0/#id3
    return StrictVersion(django.get_version()) >= StrictVersion(version)


string_format = lazy(_string_format, str)
django_3_allowed = _check_version('3.0.0')
