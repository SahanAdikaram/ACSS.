from django import template

register = template.Library()

@register.filter
def get_choice_text(value, choices):
    if isinstance(choices, dict):
        return choices.get(value, value)
    return value
