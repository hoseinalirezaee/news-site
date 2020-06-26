from .base import MehrBaseSpider
from ..base import CrawlMixin, TopNewsMixin


class MehrTopNews(CrawlMixin, TopNewsMixin, MehrBaseSpider):
    name = 'mehr-top-news'

    start_urls = ['https://www.mehrnews.com/']
    links_xpath = '((//*[@id="box1"])|(//*[@id="box2"]))//figure/a/@href'
    follow_link = True
