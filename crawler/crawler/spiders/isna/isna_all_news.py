from .base import IsnaBaseSpider
from ..base import AllNewsMixin


class IsnaAllNews(AllNewsMixin, IsnaBaseSpider):
    name = 'isna-all-news'

    archive_url = 'http://www.isna.ir/page/archive.xhtml'
    links_xpath = '//div[@class="items"]/.//h3/a/@href'
    days = 1

    def get_date_query_parameter(self, filter_date):
        return {
            'date': filter_date.strftime('%Y-%m-%d')
        }

    def get_page_query_parameter(self, page):
        return {
            'pi': page
        }
