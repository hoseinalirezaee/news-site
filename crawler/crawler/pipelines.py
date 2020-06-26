import json
import logging

import requests
from fastjsonschema import JsonSchemaException
from scrapy.exceptions import DropItem

from .json.validator import validate


class ValidatorPipeline:

    def process_item(self, item, spider):
        try:
            return validate(item)
        except JsonSchemaException:
            raise DropItem


class SendPipeline:

    def __init__(self, api_url, api_credential):
        self.api_url = api_url
        self.credential = api_credential
        self.posts = []
        self.logger = logging.getLogger('%s.SendPipeline' % __name__)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            api_url=settings.get('API_URL'),
            api_credential=settings.get('API_CREDENTIAL')
        )

    def process_item(self, item, spider):
        self.posts.append(item)
        return item

    def close_spider(self, spider):
        if self.posts:
            res = requests.post(
                url=self.api_url,
                headers={
                    'Authorization': self.credential,
                    'Content-type': 'application/json'
                },
                data=json.dumps(self.posts, ensure_ascii=False).encode('utf-8')
            )
            if res.status_code >= 300:
                self.logger.info('%s', res.text)
