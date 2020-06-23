from .base import IrnaBaseSpider


class IrnaTopNews(IrnaBaseSpider):
    name = 'irna_top_news'

    start_urls = ['https://www.irna.ir/rss-homepage']

    def parse(self, response):
        links = response.xpath('//item/link/text()').getall()
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
