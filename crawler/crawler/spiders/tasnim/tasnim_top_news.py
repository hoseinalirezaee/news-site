from .base import TasnimBaseSpider
from ..base import CrawlMixin, TopNewsMixin


class TasnimTopNews(CrawlMixin, TopNewsMixin, TasnimBaseSpider):
    name = 'tasnim-top-news'

    start_urls = ['https://www.tasnimnews.com/']
    links_xpath = '//*[@class="first"]//a/@href'
    follow_link = True
