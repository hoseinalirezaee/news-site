from .base import FarsBaseSpider
from ..base import CrawlMixin


class FarsLatestNews(CrawlMixin, FarsBaseSpider):
    name = 'farsnews-latest-news'

    start_urls = ['https://www.farsnews.ir/rss']
    follow_link = False
    links_xpath = '//item/link/text()'
