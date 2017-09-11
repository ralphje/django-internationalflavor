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


def _compare_locale_str(value):
    # In PY2, strxfrm does not support unicode encoded values, so we have to get creative.
    if not six.PY2:
        return locale.strxfrm(force_text(value))
    else:
        return _compare_by_strcoll(force_text(value))


def _compare_str(value):
    return _compare_locale_str(value)


def _option_label_getter(item):
    # For <=1.10
    # Sort optgroups above other items by putting them in a tuple
    if isinstance(item[1], (list, tuple)):
        return 0, _compare_str(item[0])
    else:
        return 1, _compare_str(item[1])


def _ctxt_optgroup_label_getter(item):
    # For >=1.11
    # we sort optgroups by sorting None below their unicode comparison (using a tuple for that)
    # because optgroup None may occur more than once, we sort these by the label of the first item in the optgroup
    if item[0] is None:
        return 1, _compare_str(item[1][0]['label'])
    else:
        return 0, _compare_str(item[0])


class SortedSelect(forms.Select):
    """A Select widget that sorts its contents by value upon rendering."""

    def get_context(self, name, value, attrs=None):
        """Overrides the rendering of options starting Django 1.11"""
        context = super(forms.Select, self).get_context(name, value, attrs)
        # we sort options in optgroups by their unicode comparison
        # optgroups themselves are ordered by their label (if any) or the first item of the group
        context['widget']['optgroups'] = sorted([(a, sorted(choices, key=lambda o: _compare_str(o['label'])), c)
                                                 for a, choices, c in context['widget']['optgroups']],
                                                key=_ctxt_optgroup_label_getter)
        return context

    def render_options(self, *args):
        """Overrides the rendering of options in Django 1.10 and prior versions"""
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
