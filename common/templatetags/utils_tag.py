from django import template
import datetime

register = template.Library()

@register.filter(name="convert_duration")
def convert_duration(value):
    if not value:
        value = 0
    return str(datetime.timedelta(minutes=value))
