from django import template
from django.db.models import Count, F, Q

register = template.Library()

@register.filter
def in_group(user, group_name):
    # print(user.groups.all())
    print(group_name)
    # print(user.groups.filter(name=group_name).exists())
    return user.groups.filter(name=group_name).exists() or group_name == ''