# -*- coding: utf-8 -*-
import scrapy
from ximalaya.items import XimalayaItem
import json


class XiSpider(scrapy.Spider):
    name = 'xi'
    allowed_domains = ['ximalaya.com']
    media = ''    # 记录音频链接的
    num = ''       # 充当一个变量，记录音频的名字！
    list_name = []
    move = 0
    media_ur = 'https://www.ximalaya.com/revision/play/tracks?trackIds='  # 音频下载前半部分链接
    url = 'https://www.ximalaya.com/youshengshu/3161070/'
    offset = 1
    start_urls = [url]

    def parse(self, response):
        self.list_name = []
        self.move = 0
        for each in response.xpath('//div[@class="dOi2 text"]'):
            # item = XimalayaItem()
            title = each.xpath('./a/text()').extract()[0]  # 超品相师0003（新书求顶，求赞，求打赏！）
            # num = title.split('师')
            # num = list(num[1])[0:4]
            # num = ''.join(num)
            # print(num)
            ur = each.xpath('./a/@href').extract()[0]  # /youshengshu/3160816/10494941
            ur = ur.split('/')[-1]   # 10494941
            self.media = self.media_ur + str(ur)
            print(self.media)
            # yield item
            yield scrapy.Request(url=self.media, callback=self.parse_media)

    def parse_media(self, response):
        data = json.loads(response.text)['data']['tracksForAudioPlay'][0]
        item = XimalayaItem()
        item['media_url'] = data['src']

        title = data['trackName']
        # 《大主宰》第5集 柳阳(新书，一念永恒！欢迎收听！)
        num = title.split('第')
        num = num[1].split('集')[0]      # 解析出来章节音频的名字
        # num = list(num[1])[0:4]
        # name = ''.join(num)
        name = num
        item['name'] = name
        print(item['media_url'])
        yield item
        if self.offset < 34:
            self.offset += 1
        yield scrapy.Request(url=self.url + 'p' + str(self.offset), callback=self.parse)
