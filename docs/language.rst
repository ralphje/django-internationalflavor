========
Language
========
.. module:: internationalflavor.language

Django already has excellent support for internationalization, but there's currently no built-in field to store the
user's language (though there is
`middleware that can take the user's locale from the browser
<https://docs.djangoproject.com/en/dev/ref/middleware/#django.middleware.locale.LocaleMiddleware>`_). This module
provides a field that allows you to store the user's language in his profile.

All languages defined in the CLDR are defined in this module. Note that CLDR will use names such as ``zh-Hans``, though
we normalize that to all-lowercase, i.e. ``zh-hans``, as this is how Django stores language codes.

.. autoclass:: internationalflavor.language.models.LanguageField
.. autoclass:: internationalflavor.language.forms.LanguageFormField

Middlware
=========
As a convenience, this module provides a middleware class that ensures your user's language is applied across your app.
If you customize your user model to include a ``language`` field, e.g.::

    class MyUser(auth_base.AbstractBaseUser, auth.PermissionsMixin)::
        language = LanguageField()

You can use it by adding
``internationalflavor.language.middleware.UserLanguageMiddleware`` to your ``MIDDLEWARE`` setting::

    MIDDLEWARE = [
        ...
        'django.middleware.locale.LocaleMiddleware',
        'internationalflavor.language.middleware.UserLanguageMiddleware',
    ]
