import re
from datetime import datetime

import pytz
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.http import Request

id_pattern = re.compile(r'/(\d+)/')


class MehrSpider(Spider):
    name = 'mehr-website-standalone-page'

    def start_requests(self):
        for i in range(500):
            yield Request(
                url='https://www.mehrnews.com/archive?pi=%d' % (i + 1)
            )

    def parse(self, response):
        links = response.xpath('//li[@class="news"]//h3/a/@href').getall()
        requests = response.follow_all(links, callback=self.parse_page)
        for request in requests:
            yield request

    def parse_page(self, response):
        title = response.xpath('//h1[@class="title"]/a/text()').get()
        post_url = response.xpath('//input[@class="clean"]/@value').get()
        summary = response.xpath('//p[@itemprop="description"]/text()').get()
        main_image = response.xpath('//img[@itemprop="image"]/@src').get()
        category = response.xpath('//ol[@class="breadcrumb"]/li[last()]/a/text()').get()

        date_time = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        date_time = pytz.timezone('utc').localize(date_time)
        date_time = date_time.isoformat()

        post_id = re.search(id_pattern, response.url).group(1)

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

        data = {}

        if title:
            data['title'] = title.strip()

        if 'http' not in post_url:
            post_url = 'https://%s' % post_url
        data['postUrl'] = post_url
        if summary:
            data['summary'] = summary.strip()

        data['mainImage'] = main_image
        if category:
            data['category'] = category.strip()
        data['dateTime'] = date_time
        data['postId'] = int(post_id)

        data['paragraphs'] = paragraphs
        data['tags'] = tags
        data['agencyCode'] = 'mehrnews'
        data['agencyTitle'] = 'خبرگزاری مهر'

        return data
