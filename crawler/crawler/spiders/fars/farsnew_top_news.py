from .base import FarsBaseSpider


class FarsTopNews(FarsBaseSpider):
    name = 'farsnews_top_news'

    start_urls = ['https://www.farsnews.ir/']

    def parse(self, response):
        links = response.xpath('//*[contains(@*, "top-news")]//a/@href').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
