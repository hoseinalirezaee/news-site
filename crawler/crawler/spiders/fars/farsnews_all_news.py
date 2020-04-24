from .base import FarsBaseSpider
from ..base import AllNewsMixin


class FarsAllNewsSpider(AllNewsMixin, FarsBaseSpider):
    name = 'fars-all-news'

    days = 60
    links_xpath = '//ul[contains(@class, "last-news")]/li/a/@href'
    archive_url = 'https://www.farsnews.ir/archive'

    def get_date_query_parameter(self, filter_date):
        return {
            'date': filter_date.strftime('%Y/%m/%d')
        }

    def get_page_query_parameter(self, page):
        return {
            'p': page
        }
