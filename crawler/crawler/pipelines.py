from fastjsonschema import JsonSchemaException
from scrapy.exceptions import DropItem

from .json.validator import validate


class ValidatorPipeline:

    def process_item(self, item, spider):
        try:
            return validate(item)
        except JsonSchemaException:
            raise DropItem
