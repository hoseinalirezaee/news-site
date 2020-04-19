import json
import os

from django.core.management import BaseCommand

from db import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            'categories.json')

        with open(categories_file_path) as categories_file:
            categories_json = json.load(categories_file)
            for root_category in categories_json:
                root, created = models.Category.objects.get_or_create(
                    title=root_category['title']
                )
                for sub_category in root_category['sub_categories']:
                    sub, created = models.Category.objects.get_or_create(
                        title=sub_category
                    )
                    if created:
                        sub.parent = root
                    sub.save()
