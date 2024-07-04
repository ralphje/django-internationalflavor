import locale
from django import forms


try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text


def _compare_locale_str(value):
    return locale.strxfrm(force_text(value))


def _compare_str(value):
    return _compare_locale_str(value)


def _option_label_getter(item):
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
