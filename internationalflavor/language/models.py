from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .forms import LanguageFormField
from .data import LANG_MAX_LENGTH, get_languages_lazy


class LanguageField(models.CharField):
    """A model field that allows users to choose their language. By default, all languages that are defined in your
    settings file are available. Use the ``langagues`` argument to specify your own langagues, and use ``exclude``
    to exclude specific languages.
    """

    description = _('A language')

    def __init__(self, languages=None, exclude=None, *args, **kwargs):
        if languages is None:
            languages = settings.LANGUAGES

        self.languages = languages
        self.exclude = exclude if exclude else []

        kwargs.setdefault('max_length', LANG_MAX_LENGTH)
        kwargs['choices'] = get_languages_lazy(languages, exclude)

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.languages != settings.LANGUAGES:
            kwargs['languages'] = self.languages
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if 'max_length' in kwargs and kwargs["max_length"] == LANG_MAX_LENGTH:
            del kwargs["max_length"]
        if "choices" in kwargs:
            del kwargs["choices"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': LanguageFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
