from .base import TasnimBaseSpider
from ..base import AllNewsMixin


class TasnimAllNews(AllNewsMixin, TasnimBaseSpider):
    name = 'tasnim-all-news'

    archive_url = 'https://www.tasnimnews.com/fa/archive'
    links_xpath = '//article[contains(@class, "list-item")]/a/@href'
    days = 1

    def get_date_query_parameter(self, filter_date):
        return {
            'date': filter_date.strftime('%Y/%m/%d')
        }

    def get_page_query_parameter(self, page):
        return {
            'page': page
        }
