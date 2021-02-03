from base64 import b64encode

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']

NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

ITEM_PIPELINES = {
    'crawler.pipelines.ValidatorPipeline': 1,
    'crawler.pipelines.SendPipeline': 2
}

FEED_EXPORT_ENCODING = 'utf-8'

API_URL = 'http://web:8000/api/interface/posts/'

user_pass = '%s:%s' % ('username', 'password')
user_pass = user_pass.encode('utf-8')
user_pass = b64encode(user_pass)
user_pass = user_pass.decode('utf-8')
API_CREDENTIAL = 'BASIC %s' % user_pass
