from django import forms
from .data import get_languages_lazy
from ..forms import SortedSelect


class LanguageFormField(forms.TypedChoiceField):
    widget = SortedSelect

    def __init__(self, languages=None, exclude=None, *args, **kwargs):
        if 'choices' not in kwargs or not kwargs['choices']:
            kwargs['choices'] = get_languages_lazy(languages, exclude)

        super().__init__(*args, **kwargs)
