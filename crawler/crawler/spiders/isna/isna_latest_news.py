from .base import IsnaBaseSpider


class IsnaLatestNews(IsnaBaseSpider):
    name = 'isna_latest_news'

    start_urls = ['https://www.isna.ir/rss']

    def parse(self, response):
        links = response.xpath('//item/link/text()').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
