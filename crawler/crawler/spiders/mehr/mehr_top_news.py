from .base import MehrBaseSpider


class MehrTopNews(MehrBaseSpider):
    name = 'mehr_top_news'

    start_urls = ['https://www.mehrnews.com/']

    def parse(self, response):
        links = response.xpath('((//*[@id="box1"])|(//*[@id="box2"]))//figure/a/@href').getall()
        for link in links:
            yield response.follow(
                link, callback=self.parse_page
            )
