from scrapy import Spider

from ..base import ParsePageMixin


class IrnaBaseSpider(ParsePageMixin, Spider):
    website_url = 'https://www.irna.ir/'

    title_xpath = '//h1[@class="title"]/a/text()'
    summary_xpath = '//meta[@name="description"]/@content'
    tags_xpath = '//section[@class="box tags d-none d-lg-block"]//a/text()'

    published_date_xpath = '//meta[@itemprop="datePublished"]/@content'
    published_date_input_format = '%Y-%m-%dT%H:%M:%SZ'

    main_image_xpath = '//figure[@class="item-img"]/img/@src'
    post_url_xpath = '//div[@class="short-link-container"]//input/@value'
    post_id_xpath = '//div[@class="item-code"]/span[last()]/text()'
    category_xpath = '//ol[@class="breadcrumb vertical"]/li[last()]/a/text()'
    agency_title = 'خبرگزاری ایرنا'
    agency_code = 'irna'
    paragraphs_selector_xpath = '//div[@itemprop="articleBody"]/p'
