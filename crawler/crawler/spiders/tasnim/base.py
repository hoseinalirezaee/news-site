import re

from scrapy import Spider

from ..base import ParsePageMixin

post_id_pattern = re.compile(r'/(\d{5,})/')
remove_fractional_pattern = re.compile(r'\..*')


class TasnimBaseSpider(ParsePageMixin, Spider):
    website_url = 'https://www.tasnimnews.com/'

    title_xpath = '//h1[@class="title"]/text()'
    summary_xpath = '//meta[@name="description"]/@content'
    tags_xpath = '(//ul[@class="smart-keyword"])[last()]/li/a/text()'

    published_date_input_format = '%Y-%m-%dT%H:%M:%S'

    main_image_xpath = '//div/figure/a/img/@src'
    post_url_xpath = '//a[@id="short-link"]/@href'
    post_id_xpath = None
    category_xpath = '//li[@class="service"][last()]/a/text()'
    agency_title = 'خبرگزاری تسنیم'
    agency_code = 'tasnimnews'
    paragraphs_selector_xpath = '//div[@class="story"]//p'

    def get_published_date(self, response):
        import json
        meta_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        meta_json = json.loads(meta_json)
        date_time = re.sub(remove_fractional_pattern, '', meta_json['datePublished'])
        return self._normalize_date_time(date_time)

    def get_post_id(self, response):
        post_id = re.findall(post_id_pattern, response.url).pop()
        return int(post_id)
