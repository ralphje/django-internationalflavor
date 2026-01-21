from django import template
from internationalflavor.iban.validators import IBANCleaner


register = template.Library()


@register.filter
def format_iban(iban):
    return IBANCleaner().display_value(iban)
