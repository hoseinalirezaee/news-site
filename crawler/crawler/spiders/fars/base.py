from scrapy import Spider

from ..base import ParsePageMixin


class FarsBaseSpider(ParsePageMixin, Spider):
    website_url = 'https://farsnews.ir'
    title_xpath = '//div[contains(@class, "news-box")]//span[contains(@class, "title")]/text()'
    summary_xpath = '//div[contains(@class, "news-box")]//p[contains(@class, "lead")]/text()'
    main_image_xpath = '//div[contains(@class, "news-box")]//div[@class="top"]/img/@src'
    tags_xpath = '//div[contains(@class, "news-box")]//div[contains(@class, "tags")]/a/text()'
    post_id_xpath = '//meta[@name="Fna.oid"]/@content'

    published_date_xpath = '//meta[@name="dc.Date"]/@content'
    published_date_input_format = '%m/%d/%Y %I:%M:%S %p'
    published_date_input_timezone = 'Asia/Tehran'

    category_xpath = '//div[contains(@class, "category-name")]//span[last()]/a/text()'
    post_url_xpath = '//span[@id="surl2"]/text()'
    paragraphs_selector_xpath = '//div[contains(@class, "nt-body")]/p'
    agency_code = 'farsnews'
    agency_title = 'خبرگزاری فارس'
