BOT_NAME = 'luoo'

SPIDER_MODULES = ['luoo.spiders']
NEWSPIDER_MODULE = 'luoo.spiders'

USER_AGENT = 'luoo (study of scrapy.)'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'luoo.pipelines.MongoPipeline': 300,
}
