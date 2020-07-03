from .base import MehrBaseSpider
from ..base import AllNewsMixin


class MehrAllNews(AllNewsMixin, MehrBaseSpider):
    name = 'mehr-all-news'

    archive_url = 'https://www.mehrnews.com/page/archive.xhtml'
    links_xpath = '//li[@class="news"]//h3/a/@href'
    days = 7

    def get_date_query_parameter(self, filter_date):
        return {
            'date': filter_date.strftime('%Y-%m-%d')
        }

    def get_page_query_parameter(self, page):
        return {
            'pi': page
        }
