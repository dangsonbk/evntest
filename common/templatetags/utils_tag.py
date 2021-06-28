from django import template
from quiz.forms import BRANCH_CHOICES

import datetime

register = template.Library()


@register.filter(name="branch_mapping")
def branch_mapping(value):
    mapping = dict(BRANCH_CHOICES)
    return mapping[value] if value in mapping else ""


@register.filter(name="convert_duration")
def convert_duration(value):
    if not value:
        value = 0
    return str(datetime.timedelta(minutes=value))
