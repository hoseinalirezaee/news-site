from .base import IrnaBaseSpider


class IrnaLatestNews(IrnaBaseSpider):
    name = 'irna_latest_news'

    start_urls = ['https://www.irna.ir/rss']

    def parse(self, response):
        links = response.xpath('//item/link/text()')
        for link in links:
            yield response.follow(
                link,
                callback=self.parse_page
            )
