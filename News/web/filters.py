import django_filters

from db import models


class CategoryMultipleChoice(django_filters.ModelChoiceFilter):

    def filter(self, qs, value):
        if value is None:
            return qs

        if value.parent is None:
            return qs.filter(category__in=value.sub_categories.all())
        return qs.filter(category=value)


class PostFilterSet(django_filters.FilterSet):
    agency = django_filters.ModelChoiceFilter(queryset=models.Agency.objects.all(), label='خبرگزاری')
    category = CategoryMultipleChoice(queryset=models.Category.objects.all(), label='دسته‌بندی')

    class Meta:
        model = models.Post
        fields = ['agency', 'category']
