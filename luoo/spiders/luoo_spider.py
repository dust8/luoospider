from scrapy import Spider, Request
from luoo.items import LuooItem


class LuooSpider(Spider):
    name = 'luoo'
    allowed_domains = ['luoo.net']
    start_urls = ['http://www.luoo.net/music/']

    def __init__(self, last_vol_number=0, *args, **kwargs):
        super(LuooSpider, self).__init__(*args, **kwargs)
        # 上次抓取的最大期刊期号
        self.last_vol_number = last_vol_number
        self.stop = False

    def parse(self, response):
        # 抓取一页里面的每期期刊地址
        for href in response.css('div.vol-list>div.item>a::attr("href")'):
            url = href.extract()
            if url.split('/')[-1] <= self.last_vol_number:
                self.stop = True
                break
            yield Request(url, callback=self.parse_vol_contents)

        # 抓取下一页地址
        if not self.stop:
            for href in response.css('a.next::attr("href")'):
                url = href.extract()
                yield Request(url, callback=self.parse)

    def parse_vol_contents(self, response):
        '''抓取一期期刊里面的内容
        '''
        vol_number = response.css('span.vol-number::text').extract_first()
        vol_title = response.css('span.vol-title::text').extract_first()

        for sel in response.xpath('//div[contains(@class, "vol-tracklist")]/ul/li'):
            item = LuooItem()
            item['vol_number'] = vol_number
            item['vol_title'] = vol_title
            item['trackname'] = sel.css(
                'div.track-wrapper>a.trackname::text').extract_first()
            item['artist'] = sel.css(
                'div.track-wrapper>span.artist::text').extract_first()
            yield item
