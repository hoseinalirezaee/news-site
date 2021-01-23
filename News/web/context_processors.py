from db import models


def get_root_categories(request):
    categories = models.Category.objects.all().cache()
    data = {}

    for category in categories:
        if category.parent is not None:
            try:
                list = data[category.parent]
                list.append(category)
            except KeyError:
                data[category.parent] = [category]

    return {'categories': data}
