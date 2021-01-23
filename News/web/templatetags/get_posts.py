import random

from django.template.library import Library

from db import models

register = Library()

choices = [1, 3, 5]


@register.filter
def get_posts(category):
    queryset = models.Post.objects.all().filter(
        category__in=category.sub_categories.all()) if not category.parent else category.posts

    data = []

    if len(queryset) < 8:
        for post in queryset:
            data.append(
                {
                    'type': 1,
                    'items': post
                }
            )
    else:
        start_index = 1

        data.append(
            {
                'type': 1,
                'items': queryset[0]
            }
        )

        for _ in range(2):
            type_number = random.choice(choices)

            if start_index >= len(queryset) or start_index + type_number >= len(queryset):
                break

            data.append(
                {
                    'type': type_number,
                    'items': queryset[start_index: start_index + type_number] if type_number != 1 else queryset[
                        start_index]
                }
            )
            start_index += type_number

        data.append(
            {
                'type': 1,
                'items': queryset[start_index]
            }
        )

    return data
