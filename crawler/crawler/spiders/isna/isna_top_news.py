from .base import IsnaBaseSpider
from ..base import CrawlMixin, TopNewsMixin


class IsnaTopNews(CrawlMixin, TopNewsMixin, IsnaBaseSpider):
    name = 'isna-top-news'

    start_urls = ['https://www.isna.ir/']
    links_xpath = '(//section[contains(@class,"box top slider")])[1]//a/@href'
    follow_link = True
