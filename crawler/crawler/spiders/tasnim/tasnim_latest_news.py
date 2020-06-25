from scrapy import Request

from .base import TasnimBaseSpider


class TasnimLatestNews(TasnimBaseSpider):
    name = 'tasnim_latest_news'

    start_urls = [
        'https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2']

    def parse(self, response):
        links = response.xpath('//item/link/text()').getall()
        for link in links:
            yield Request(
                link,
                callback=self.parse_page
            )
