from .base import IrnaBaseSpider
from ..base import TopNewsMixin, CrawlMixin


class IrnaTopNews(TopNewsMixin, CrawlMixin, IrnaBaseSpider):
    name = 'irna-top-news'

    start_urls = ['https://www.irna.ir/rss-homepage']
    follow_link = True
    links_xpath = '//item/link/text()'
