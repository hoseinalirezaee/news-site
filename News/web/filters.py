import django_filters

from db import models


class CategoryMultipleChoice(django_filters.ModelChoiceFilter):

    def filter(self, qs, value):
        if value is None:
            return qs

        if value.parent is None:
            return qs.filter(category__in=value.sub_categories.all().cache(timeout=60 * 60 * 24 * 15))
        return qs.filter(category=value).cache()


class SearchFiler(django_filters.CharFilter):
    def filter(self, qs, value):
        if value in ['', None]:
            return qs
        return qs.filter(title__search=value).cache()


class PostFilterSet(django_filters.FilterSet):
    agency = django_filters.ModelChoiceFilter(queryset=models.Agency.objects.all().cache(timeout=60 * 60 * 24 * 15),
                                              label='خبرگزاری')
    category = CategoryMultipleChoice(queryset=models.Category.objects.all().cache(timeout=60 * 60 * 24 * 15),
                                      label='دسته‌بندی')
    query = SearchFiler(label='')

    class Meta:
        model = models.Post
        fields = ['agency', 'category']
