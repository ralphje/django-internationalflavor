from itertools import chain
import locale
from django import forms
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import format_html


class _compare_by_strcoll(object):
    __slots__ = ['obj']

    def __init__(self, obj, *args):
        self.obj = obj

    def __lt__(self, other):
        return locale.strcoll(self.obj, other.obj) < 0

    def __gt__(self, other):
        return locale.strcoll(self.obj, other.obj) > 0

    def __eq__(self, other):
        return locale.strcoll(self.obj, other.obj) == 0

    def __le__(self, other):
        return locale.strcoll(self.obj, other.obj) <= 0

    def __ge__(self, other):
        return locale.strcoll(self.obj, other.obj) >= 0

    def __ne__(self, other):
        return locale.strcoll(self.obj, other.obj) != 0

    def __hash__(self):
        raise TypeError('hash not implemented')


def _option_label_getter(item):
    result = force_text(item[0] if isinstance(item[1], (list, tuple)) else item[1])
    # In PY2, strxfrm does not support unicode encoded values, so we have to get creative.
    if six.PY3:
        return locale.strxfrm(result)
    else:
        return _compare_by_strcoll(result)


class SortedSelect(forms.Select):
    """A Select widget that sorts its contents by value upon rendering."""

    def render_options(self, *args):
        try:
            selected_choices, = args
        except ValueError:  # Signature contained `choices` prior to Django 1.10
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices

        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in sorted(choices, key=_option_label_getter):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
                for option in sorted(option_label, key=_option_label_getter):
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)
