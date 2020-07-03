from .base import MehrBaseSpider
from ..base import CrawlMixin


class MehrLatestNews(CrawlMixin, MehrBaseSpider):
    name = 'mehr-latest-news'

    start_urls = ['https://www.mehrnews.com/rss']
    links_xpath = '//item/link/text()'
    follow_link = True
