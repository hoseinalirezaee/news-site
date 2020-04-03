import re

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

    # def start_requests(self):
    #     for i in range(10):
    #         yield Request(
    #             f'https://www.mehrnews.com/page/archive.xhtml?pi={i}',
    #             callback=self.parse_archive
    #         )

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
        data['tags'] = tags

        yield data

    # def parse_archive(self, response):
    #     links = response.xpath('//li[@class="news"]/.//a/@href').getall()
    #     for link in links:
    #         yield Request(
    #             'https://www.mehrnews.com' + link,
    #             callback=self.parse
    #         )

    # def parse(self, response):
    #
    #     title = response.xpath('//h1[@class="title"]/a/text()').get()
    #     summary = response.xpath('//p[@itemprop="description"]/text()').get()
    #     main_image = response.xpath('//img[@itemprop="image"]/@src').get()
    #     post_id = response.xpath('//div[@class="item-code"]/span/text()').get()
    #     post_url = response.xpath('//div[@class="short-link-container"]/.//input/@value').get()
    #     tags = response.xpath('//section[contains(@class, "tag")]/.//a/text()').getall()
    #     category = response.xpath('//div[@class="item-header"]/.//ol[@class="breadcrumb"]/.//a/text()').getall()[1]
    #     date = response.xpath('//div[contains(@class, "item-date")]/span/text()').get()
    #     datetime = MehrnewsSpider.str_to_date(date)
    #     paragraphs = []
    #
    #     paragraphs_selector = response.xpath('//div[@itemprop="articleBody"]/p')
    #     for p in paragraphs_selector:
    #         image = p.xpath('.//img')
    #         if image:
    #             image_url = image.xpath('./@src').get()
    #             paragraphs.append(
    #                 {
    #                     'type': 'image',
    #                     'data': image_url.strip()
    #                 }
    #             )
    #         else:
    #             bs = BeautifulSoup(p.get(), features='lxml')
    #             text = bs.text
    #             if text and text.strip():
    #                 paragraphs.append(
    #                     {
    #                         'type': 'text',
    #                         'data': text.strip()
    #                     }
    #                 )
    #
    #     yield {
    #         'title': title.strip(),
    #         'summary': summary.strip(),
    #         'dateTime': str(datetime),
    #         'mainImage': main_image.strip(),
    #         'paragraphs': paragraphs,
    #         'postId': int(post_id),
    #         'postUrl': post_url.strip(),
    #         'tags': tags,
    #         'category': category.strip()
    #     }

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
