# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ximalaya.items import XimalayaItem
import json


class XimaSpider(CrawlSpider):
    name = 'xima'
    allowed_domains = ['ximalaya.com']
    url = 'https://www.ximalaya.com/revision/play/tracks?trackIds='   # 音频下载前半部分链接
    media_number = ''  # 音频链接的后半部分
    start_urls = ['https://www.ximalaya.com/youshengshu/18349720/']
    page_links = LinkExtractor(allow=r'/.+/\d+/p\d+/')     # /youshengshu/3160816/p70/
    # mp4_links = LinkExtractor(allow=r'')
    rules = (
        Rule(page_links, process_links='deal_links', callback='parse_page'),
    )

    # 由于翻页page的连接少了一部分，所以自己就的加上了，不然访问不了！
    def deal_links(self, links):
        for each in links:
            each.url = 'https://www.ximalaya.com/' + each.url
        return links

    # 接下来就来解析音频链接了！
    def parse_page(self, response):
        for each in response.xpath('//div[@class="dOi2 text"]'):
            item = XimalayaItem()
            title = each.xpath('./a/text()')  # 超品相师0003（新书求顶，求赞，求打赏！）
            # num = title.split('师')
            # num = list(num[1])[0:4]
            # num = ''.join(num)
            # print(num)
            item['name'] = title
            ur = each.xpath('./a/@href')  # /youshengshu/3160816/10494941
            ur = ur.split('/')[-1]
            self.media_number = ur
            yield item

        yield scrapy.Request(self.url+str(self.media_number), callback=self.parse_media)

    def parse_media(self, response):
        data = json.loads(response.text())['data']
        item = XimalayaItem()
        item['media_url'] = data['tracksForAudioPlay'][0]['src']
        print(item['media_url'])
        # yield item
