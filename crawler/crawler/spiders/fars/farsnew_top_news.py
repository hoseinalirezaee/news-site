from .base import FarsBaseSpider
from ..base import CrawlMixin, TopNewsMixin


class FarsTopNews(CrawlMixin, TopNewsMixin, FarsBaseSpider):
    name = 'farsnews-top-news'

    start_urls = ['https://www.farsnews.ir/']
    links_xpath = '//*[contains(@*, "top-news")]//a/@href'
    follow_link = True
