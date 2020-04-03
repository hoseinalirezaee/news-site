import re
from datetime import datetime

import jdatetime
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import XMLFeedSpider

from crawler.common.dateconvertor import month_str_to_int

id_pattern = re.compile(r'/(\d+)/')
category_pattern = re.compile(r'>(.+)$')


class MehrnewsSpider(XMLFeedSpider):
    name = 'mehrnews'

    start_urls = ['https://www.mehrnews.com/rss']
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
        data['dateTime'] = selector.xpath('pubDate/text()').get()
        data['dateTime'] = datetime.strptime(data['dateTime'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')
        data['postId'] = re.search(id_pattern, post_url).group(1)

        return Request(
            data['postUrl'],
            callback=self.parse_page,
            cb_kwargs={'data': data}
        )

    def parse_page(self, response, data):
        tags = response.xpath('//section[contains(@class, "tag")]/.//a/text()').getall()
        paragraphs = []
        paragraphs_selector = response.xpath('//div[@itemprop="articleBody"]/p')
        for p in paragraphs_selector:
            image = p.xpath('.//img')
            if image:
                image_url = image.xpath('./@src').get()
                paragraphs.append(
                    {
                        'type': 'image',
                        'body': image_url.strip()
                    }
                )
            else:
                bs = BeautifulSoup(p.get(), features='lxml')
                text = bs.text
                if text and text.strip():
                    paragraphs.append(
                        {
                            'type': 'text',
                            'body': text.strip()
                        }
                    )

        data['paragraphs'] = paragraphs
        data['tags'] = tags
        data['agencyCode'] = 'mehrnews'
        data['agencyTitle'] = 'خبرگزاری مهر'

        yield data

    @staticmethod
    def str_to_date(str):
        date = list(filter(None, re.split(r'[- :]', str)))
        date[1] = month_str_to_int[date[1]]
        for i in range(len(date)):
            date[i] = int(date[i])
        persian_datetime = jdatetime.datetime(
            date[2],
            date[1],
            date[0],
            date[3],
            date[4]
        )

        return persian_datetime.togregorian()
