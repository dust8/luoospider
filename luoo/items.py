import scrapy


class LuooItem(scrapy.Item):
    vol_number = scrapy.Field()
    vol_title = scrapy.Field()
    trackname = scrapy.Field()
    artist = scrapy.Field()
