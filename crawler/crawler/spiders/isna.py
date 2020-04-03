import re

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import XMLFeedSpider

id_pattern = re.compile(r'/(\d+)/')
category_pattern = re.compile(r'>(.+)$')


class IsnaSpider(XMLFeedSpider):
    name = 'isna'
    start_urls = ['https://www.isna.ir/rss']
    itertag = 'item'

    def parse_node(self, response, selector):

        post_url = selector.xpath('link/text()').get()
        raw_category = selector.xpath('category/text()').get()
        data = dict()
        data['title'] = selector.xpath('title/text()').get()
        data['postUrl'] = post_url
        data['summary'] = selector.xpath('description/text()').get()
        data['mainImage'] = selector.xpath('enclosure/@url').get()
        data['category'] = re.search(category_pattern, raw_category).group(1).strip()
        data['dataTime'] = selector.xpath('pubDate/text()').get()
        data['postId'] = re.search(id_pattern, post_url).group(1)

        return Request(
            data['postUrl'],
            callback=self.parse_page,
            cb_kwargs={'data': data}
        )

    def parse_page(self, response, data):

        paragraphs = []
        paragraphs_selector = response.xpath('//div[@itemprop="articleBody"]/p')
        for p in paragraphs_selector:
            image = p.xpath('.//img')
            if image:
                image_url = image.xpath('./@src').get()
                paragraphs.append(
                    {
                        'type': 'image',
                        'data': image_url.strip()
                    }
                )
            else:
                bs = BeautifulSoup(p.get(), features='lxml')
                text = bs.text
                if text and text.strip():
                    paragraphs.append(
                        {
                            'type': 'text',
                            'data': text.strip()
                        }
                    )
            data['paragraphs'] = paragraphs
            data['tags'] = response.xpath('//footer[@class="tags"]/.//a/text()').getall()
        return data
