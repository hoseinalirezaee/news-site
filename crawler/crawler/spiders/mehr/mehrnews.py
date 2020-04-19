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


s = ['<meta itemprop="inLanguage" content="fa">',
     '<meta itemprop="name" name="twitter:title" property="dc.title" content="تولید روزانه اوپک در مارس ۸۲۱ هزار بشکه افزایش یافت">',
     '<meta name="description" property="dc.description" content="تولید روزانه نفت اعضای اوپک براساس گزارش منابع ثانویه در ماه مارس (اسفند - فروردین) نسبت به ماه فوریه (بهمن - اسفند) ۸۲۱ هزار بشکه افزایش یافت و در مجموع به ۲۸ میلیون و ۶۱۲ هزار بشکه رسید.">',
     '<meta property="og:type" content="article">',
     '<meta name="twitter:url" property="og:url" content="https://www.mehrnews.com/news/4902834/تولید-روزانه-اوپک-در-مارس-۸۲۱-هزار-بشکه-افزایش-یافت">',
     '<meta property="article:modified_time" content="2020-04-17T14:26:21Z">',
     '<meta property="article:section" content="اقتصاد &gt; آب و انرژی">',
     '<meta name="keywords" property="article:tag" content="اوپک,تولید نفت,افزایش تولید نفت">',
     '<meta property="nastooh:topic" content="Economy">', '<meta property="nastooh:subtopic" content="Water-Energy">',
     '<meta property="nastooh:pageType" content="news">', '<meta property="nastooh:newsType" content="news">',
     '<meta property="nastooh:publishDate" content="2020-04-17">',
     '<meta property="nastooh:commentCount" content="na">', '<meta property="nastooh:keywordCount" content="3">',
     '<meta property="nastooh:bodyWordCount" content="small">', '<meta property="nastooh:code" content="4902834">',
     '<meta property="nastooh:nid" content="4902834">',
     '<meta property="og:title" itemprop="headline" content="تولید روزانه اوپک در مارس ۸۲۱ هزار بشکه افزایش یافت">',
     '<meta name="twitter:description" itemprop="description" property="og:description" content="تولید روزانه نفت اعضای اوپک براساس گزارش منابع ثانویه در ماه مارس (اسفند - فروردین) نسبت به ماه فوریه (بهمن - اسفند) ۸۲۱ هزار بشکه افزایش یافت و در مجموع به ۲۸ میلیون و ۶۱۲ هزار بشکه رسید.">',
     '<meta name="thumbnail" itemprop="thumbnailUrl" content="https://media.mehrnews.com/d/2020/04/09/1/3422720.jpg">',
     '<meta name="twitter:image" itemprop="image" property="og:image" content="https://media.mehrnews.com/d/2020/04/09/4/3422720.jpg">',
     '<meta itemprop="datePublished" property="article:published_time" content="2020-04-17T14:26:21Z">',
     '<meta itemprop="dateModified" property="article:modified" content="2020-04-17T14:26:21Z">',
     '<meta name="twitter:card" content="summary_large_image">', '<meta name="genre" itemprop="genre" content="News">',
     '<meta charset="utf-8">', '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">',
     '<meta http-equiv="Content-Language" content="fa">',
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
     '<meta name="google-site-verification" content="2fSnrTNqXkhCZmioof4e4LVrRlEpS7Wm3Bq1Kk31720">',
     '<meta name="alexaVerifyID" content="W_YJ4-m0sxSKfPB_PRnHIChXnCM">',
     '<meta name="msvalidate.01" content="CE6454B7E800DF383F5334DF0BEEE12B">',
     '<meta http-equiv="content-language" content="fa">', '<meta http-equiv="refresh" content="300">',
     '<meta property="og:site_name" content="خبرگزاری مهر | اخبار ایران و جهان | Mehr News Agency">',
     '<meta property="og:locale" content="fa">', '<meta name="generator" content="www.nastooh.ir">',
     '<meta name="language" content="fa">', '<meta name="rating" content="General">',
     '<meta name="copyright" content="All Content by Mehr News Agency is licensed under a Creative Commons Attribution 4.0 International License.">',
     '<meta name="expires" content="never">',
     '<meta name="publisher" content="خبرگزاری مهر | اخبار ایران و جهان | Mehr News Agency">',
     '<meta name="dc.publisher" content="خبرگزاری مهر | اخبار ایران و جهان | Mehr News Agency">',
     '<meta name="date" content="2020-04-17 T 19:14:22 +0430">']
