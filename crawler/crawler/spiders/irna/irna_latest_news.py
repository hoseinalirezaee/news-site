from .base import IrnaBaseSpider
from ..base import CrawlMixin


class IrnaLatestNews(CrawlMixin, IrnaBaseSpider):
    name = 'irna-latest-news'

    start_urls = ['https://www.irna.ir/rss']
    links_xpath = '//item/link/text()'
    follow_link = True
