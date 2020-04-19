BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']

NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 32

ITEM_PIPELINES = {
    'crawler.pipelines.ValidatorPipeline': 1,
}

FEED_EXPORT_ENCODING = 'utf-8'
