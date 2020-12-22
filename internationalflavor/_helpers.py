from django.utils.functional import lazy


def orig_str(lazy_str):
    return lazy_str._proxy____args[0]


def _string_format(str, format):
    """
    Lazy variant of string formatting, needed for situations where string
    formatting may be evaluated before it is calculated
    """
    return str % format


string_format = lazy(_string_format, str)
