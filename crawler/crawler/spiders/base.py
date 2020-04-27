from datetime import datetime
from datetime import timedelta
from urllib.parse import urlsplit, urlunsplit, urlencode, urljoin, quote

from bs4 import BeautifulSoup
from jdatetime import date as jdate
from pytz import timezone
from scrapy import Request


class ParsePageMixin:
    website_url = None

    title_xpath = None
    summary_xpath = None
    tags_xpath = None

    published_date_xpath = None
    published_date_input_format = None
    published_date_output_format = None
    published_date_input_timezone = 'UTC'
    published_date_output_timezone = 'UTC'

    main_image_xpath = None
    post_url_xpath = None
    post_id_xpath = None
    category_xpath = None
    agency_title = None
    agency_code = None
    paragraphs_selector_xpath = None

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        if self.website_url:
            components = urlsplit(self.website_url)
            self.url_schema = components.scheme

    def parse_page(self, response):
        data = {}

        data['title'] = self.get_title(response)
        data['summary'] = self.get_summary(response)
        data['tags'] = self.get_tags(response)
        data['publishedDate'] = self.get_published_date(response)
        data['mainImage'] = self.get_main_image(response)
        data['postUrl'] = self.get_post_url(response)
        data['postId'] = self.get_post_id(response)
        data['category'] = self.get_category(response)
        data['paragraphs'] = self.get_paragraphs(response)
        data['agencyCode'] = self.agency_code
        data['agencyTitle'] = self.agency_title

        return data

    def get_title(self, response):
        if not self.title_xpath:
            raise NotImplementedError('You must either implement `get_title` or set `title_xpath`')

        title = response.xpath(self.title_xpath).get()
        if title:
            title = title.strip()
        return title or None

    def get_summary(self, response):
        if not self.summary_xpath:
            raise NotImplementedError('You must either implement `get_summary` or set `summary_xpath`')

        summary = response.xpath(self.summary_xpath).get()
        if summary:
            summary = summary.strip()
        return summary or None

    def get_tags(self, response):
        if not self.tags_xpath:
            raise NotImplementedError('You must either implement `get_tags` or set `tags_xpath`')
        tags = []
        for tag in response.xpath(self.tags_xpath).getall():
            striped_tag = tag.strip()
            if striped_tag and len(striped_tag) < 100:
                tags.append(tag.strip())
        return tags

    def get_published_date(self, response):
        if not self.published_date_xpath:
            raise NotImplementedError('You must either implement `get_published_date` or set `published_date_xpath`')

        published_date = response.xpath(self.published_date_xpath).get()
        if self.published_date_input_format:
            return self._normalize_date_time(published_date)
        return published_date

    def _normalize_date_time(self, date_time):
        date_time = datetime.strptime(date_time, self.published_date_input_format)
        tz = timezone(self.published_date_input_timezone)
        date_time = tz.localize(date_time)
        date_time = date_time.replace(microsecond=0)
        output_date_time = date_time.astimezone(tz=timezone(self.published_date_output_timezone))
        if self.published_date_output_format:
            return output_date_time.strftime(self.published_date_output_format)
        return output_date_time.isoformat()

    def get_main_image(self, response):
        if not self.main_image_xpath:
            raise NotImplementedError('You must either implement `get_main_image` or set `main_image_xpath`')

        image_url = response.xpath(self.main_image_xpath).get()
        if not image_url:
            return None
        if not urlsplit(image_url).netloc:
            image_url = urljoin(self.website_url, image_url)
        components = urlsplit(image_url)
        image_url = urlunsplit((components.scheme,
                                components.netloc,
                                quote(components.path.encode('utf-8')),
                                components.query,
                                components.fragment))

        return image_url

    def get_post_url(self, response):
        if not self.post_url_xpath:
            raise NotImplementedError('You must either implement `get_post_url` or set `post_url_xpath`')

        post_url = response.xpath(self.post_url_xpath).get()
        if not post_url:
            return None
        if 'http' not in post_url and 'https' not in post_url:
            post_url = '%s://%s' % (self.url_schema, post_url)

        return post_url

    def get_post_id(self, response):
        if not self.post_id_xpath:
            raise NotImplementedError('You must either implement `get_post_id` or set `post_id_xpath`')

        post_id = response.xpath(self.post_id_xpath).get()
        if post_id:
            post_id = int(post_id)

        return post_id

    def get_category(self, response):
        if not self.category_xpath:
            raise NotImplementedError('You must either implement `get_category` or set `category_xpath`')

        category = response.xpath(self.category_xpath).get()
        if category:
            category = category.strip()
        return category

    def get_paragraphs(self, response):
        if not self.paragraphs_selector_xpath:
            raise NotImplementedError('You must either implement `get_paragraphs` or set `paragraphs_selector_xpath`')

        paragraphs_selector = response.xpath(self.paragraphs_selector_xpath)
        paragraphs = []
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
        return paragraphs


class AllNewsMixin:
    archive_url = None
    links_xpath = None
    days = 1

    def start_requests(self):
        assert self.archive_url is not None, '`archive_url` must be set.'

        today = jdate.today()
        for i in range(self.days):
            filter_date = today - timedelta(days=i)
            query_parameter = {}
            query_parameter.update(self.get_date_query_parameter(filter_date))
            query_parameter.update(self.get_page_query_parameter(1))
            yield Request(
                url=self.archive_url + '?%s' % urlencode(query_parameter),
                callback=self.parse_archive_page,
                cb_kwargs={
                    'filter_date': filter_date,
                    'page': 1
                }
            )

    def parse_archive_page(self, response, filter_date, page):
        assert self.links_xpath is not None, 'You must set `links_xpath`.'

        links = response.xpath(self.links_xpath).getall()
        if links:
            for link in links:
                yield response.follow(link, callback=self.parse_page)

            query_parameter = {}
            query_parameter.update(self.get_date_query_parameter(filter_date))
            query_parameter.update(self.get_page_query_parameter(page + 1))

            yield Request(
                url=self.archive_url + '?%s' % urlencode(query_parameter),
                callback=self.parse_archive_page,
                cb_kwargs={
                    'page': page + 1,
                    'filter_date': filter_date
                }
            )

    def get_date_query_parameter(self, filter_date):
        raise NotImplementedError('You must implement `get_date_query_parameter`.')

    def get_page_query_parameter(self, page):
        raise NotImplementedError('You must implement `get_page_query_parameter`.')

    def get_extra_query_parameter(self):
        return {}

    def get_links(self, response):
        if self.links_xpath:
            raise NotImplementedError('You must either implement `get_links` or set `links_xpath`.')

        links = response.xpath(self.links_xpath).getall()
        return links
