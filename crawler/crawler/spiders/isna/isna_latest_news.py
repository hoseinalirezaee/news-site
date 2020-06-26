from .base import IsnaBaseSpider
from ..base import CrawlMixin


class IsnaLatestNews(CrawlMixin, IsnaBaseSpider):
    name = 'isna-latest-news'

    start_urls = ['https://www.isna.ir/rss']
    links_xpath = '//item/link/text()'
    follow_link = True
