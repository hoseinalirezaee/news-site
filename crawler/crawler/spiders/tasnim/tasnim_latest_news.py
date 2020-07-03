from .base import TasnimBaseSpider
from ..base import CrawlMixin


class TasnimLatestNews(CrawlMixin, TasnimBaseSpider):
    name = 'tasnim-latest-news'

    start_urls = [
        'https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2']
    links_xpath = '//item/link/text()'
    follow_link = False
