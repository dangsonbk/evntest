from django import template

from quiz.forms import BRANCH_CHOICES

register = template.Library()


@register.filter(name="branch_mapping")
def branch_mapping(value):
    mapping = dict(BRANCH_CHOICES)
    return mapping[value] if value in mapping else ""
