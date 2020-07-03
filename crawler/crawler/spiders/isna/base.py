from scrapy import Spider

from ..base import ParsePageMixin


class IsnaBaseSpider(ParsePageMixin, Spider):
    website_url = 'https://www.isna.ir'

    title_xpath = '//h1[@class="first-title"]/text()'
    summary_xpath = '//p[@class="summary"]/text()'
    tags_xpath = '//footer[@class="tags"]/.//a/text()'

    published_date_xpath = '//meta[@property="article:published_time"]/@content'
    published_date_input_format = '%Y-%m-%dT%H:%M:%SZ'

    main_image_xpath = '//img[@itemprop="image"]/@src'
    post_url_xpath = '//input[@id="short-url"]/@value'
    post_id_xpath = '//meta[@property="nastooh:code"]/@content'
    category_xpath = '//span[@itemprop="articleSection"]/text()'
    agency_title = 'خبرگزاری ایسنا'
    agency_code = 'isna'
    paragraphs_selector_xpath = '//div[@itemprop="articleBody"]/p'
