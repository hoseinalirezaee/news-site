from .base import IsnaBaseSpider


class IsnaTopNews(IsnaBaseSpider):
    name = 'isna-top-news'

    start_urls = ['https://www.isna.ir/']

    def parse(self, response):
        links = response.xpath('(//section[contains(@class,"box top slider")])[1]//a/@href').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
