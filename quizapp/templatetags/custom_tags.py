from django import template
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(str(key))  # Ensure key is string

@register.filter(name='get_option')
def get_option(question, option_number):
    return getattr(question, f"option{option_number}", "")

@register.filter
def mul(value, arg):
    return int(value) * int(arg)
