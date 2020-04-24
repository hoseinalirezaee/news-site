from .base import IrnaBaseSpider
from ..base import AllNewsMixin


class IrnaAllNewsSpider(AllNewsMixin, IrnaBaseSpider):
    name = 'irna-all-news'

    archive_url = 'https://www.irna.ir/archive'
    links_xpath = '//div[contains(@class, "main-content")]//h3/a/@href'
    days = 1

    def get_date_query_parameter(self, filter_date):
        return {
            'dy': filter_date.day,
            'mn': filter_date.month,
            'yr': filter_date.year
        }

    def get_page_query_parameter(self, page):
        return {
            'pi': page
        }

    def get_extra_query_parameter(self):
        return {
            'ty': 1
        }
