from django import template

register = template.Library()

@register.filter
def placeholder(value, text_to_be_placed):
    return value.as_widget(attrs={'placeholder': text_to_be_placed})