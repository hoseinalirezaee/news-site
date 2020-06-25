from .base import TasnimBaseSpider


class TasnimTopNews(TasnimBaseSpider):
    name = 'tasnim_top_news'

    start_urls = ['https://www.tasnimnews.com/']

    def parse(self, response):
        links = response.xpath('//*[@class="first"]//a/@href').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
