from scrapy import Request

from .base import FarsBaseSpider


class FarsLatestNews(FarsBaseSpider):
    name = 'farsnews_latest_news'

    start_urls = ['https://www.farsnews.ir/rss']

    def parse(self, response):
        links = response.xpath('//item/link/text()').getall()
        for link in links:
            yield Request(
                link,
                callback=self.parse_page
            )
