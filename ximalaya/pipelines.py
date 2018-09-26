# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from scrapy.conf import settings
import os


class XimalayaPipeline(object):
    IMAGES_STORE = settings['IMAGES_STORE']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2050.400',

        'Referer': 'https://www.ximalaya.com'}

    # def __init__(self):
    #     self.f = open(self.IMAGES_STORE, 'wb')

    def process_item(self, item, spider):
        audio = requests.get(item['media_url'], headers=self.headers)
        # with open(self.IMAGES_STORE, 'wb') as f:
        audio_path = self.IMAGES_STORE + '/' + str(item['name']) + '.mp4'
        # if not os.path.exists(audio_path):
        #     os.makedirs(audio_path)
        with open(audio_path, 'wb') as f:
            f.write(audio.content)
        return item

    # def close_spider(self, spider):
        # self.f.close()