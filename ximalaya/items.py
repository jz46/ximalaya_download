# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XimalayaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 章节名编号
    # media_num = scrapy.Field()   # 音频链接的后半部分
    media_url = scrapy.Field()      # 音频下载链接
