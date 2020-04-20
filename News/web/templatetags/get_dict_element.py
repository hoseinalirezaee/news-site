from django import template

register = template.Library()


@register.filter
def get_dic_element(dictionary, key):
    ret = dictionary[key]
    return ret
