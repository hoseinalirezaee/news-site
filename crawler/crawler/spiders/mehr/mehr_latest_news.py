from .base import MehrBaseSpider


class MehrLatestNews(MehrBaseSpider):
    name = 'mehr_latest_news'

    start_urls = ['https://www.mehrnews.com/rss']

    def parse(self, response):
        links = response.xpath('//item/link/text()').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
