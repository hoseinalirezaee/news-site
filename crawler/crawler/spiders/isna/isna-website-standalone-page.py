import re
from datetime import datetime

import pytz
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.http import Response
from scrapy.spiders import Spider

id_pattern = re.compile(r'/(\d+)/')
normalize_time_pattern = re.compile(r'\.\d+')
whitespace_pattern = re.compile(r'\W+')


class IsnaSpider(Spider):
    name = 'isna-website-standalone-page'

    def start_requests(self):
        for i in range(500):
            yield Request(
                url='http://www.isna.ir/page/archive.xhtml?pi=%d' % (i + 1)
            )

    def parse(self, response: Response):
        links = response.xpath('//div[@class="items"]/.//h3/a/@href').getall()
        requests = response.follow_all(links, callback=self.parse_page)
        for request in requests:
            yield request

    def parse_page(self, response):

        title = response.xpath('//h1[@class="first-title"]/text()').get()
        summary = response.xpath('//p[@class="summary"]/text()').get()
        main_image = response.xpath('//img[@itemprop="image"]/@src').get()
        category = response.xpath('//span[@itemprop="articleSection"]/text()').get()
        url = response.xpath('//input[@id="short-url"]/@value').get()
        id = re.findall(id_pattern, url).pop()

        date_time = response.xpath('//div/meta[@itemprop="datePublished"]/@content').get()
        date_time = re.sub(normalize_time_pattern, '', date_time)
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        date_time = pytz.timezone('asia/tehran').localize(date_time)
        date_time = date_time.astimezone(tz=pytz.timezone('UTC'))
        date_time = date_time.isoformat()

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

        data = {}

        if title:
            data['title'] = title.strip()
        if summary:
            data['summary'] = summary.strip()
        if category:
            data['category'] = category.strip()

        data['postUrl'] = url
        data['mainImage'] = main_image
        data['postId'] = id
        data['dateTime'] = date_time
        data['paragraphs'] = paragraphs
        data['tags'] = response.xpath('//footer[@class="tags"]/.//a/text()').getall()
        data['agencyCode'] = 'isna'
        data['agencyTitle'] = 'خبرگزاری ایسنا'

        return data
