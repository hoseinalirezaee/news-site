from scrapy import Spider

from ..base import ParsePageMixin


class MehrBaseSpider(ParsePageMixin, Spider):
    website_url = 'https://www.mehrnews.com'

    title_xpath = '//h1[@class="title"]/a/text()'
    summary_xpath = '//p[@itemprop="description"]/text()'
    tags_xpath = '//section[contains(@class, "tag")]/.//a/text()'

    published_date_xpath = '//meta[@itemprop="datePublished"]/@content'
    published_date_input_format = '%Y-%m-%dT%H:%M:%SZ'

    main_image_xpath = '//img[@itemprop="image"]/@src'
    post_url_xpath = '//input[@class="clean"]/@value'
    post_id_xpath = '//meta[@property="nastooh:nid"]/@content'
    category_xpath = '//ol[@class="breadcrumb"]/li[last()]/a/text()'
    agency_title = 'خبرگزاری مهر'
    agency_code = 'mehrnews'
    paragraphs_selector_xpath = '//div[@itemprop="articleBody"]/p'
