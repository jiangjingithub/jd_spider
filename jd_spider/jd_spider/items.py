# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 商品名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 评论数
    comment_num = scrapy.Field()
    # 评论内容
    comment_content = scrapy.Field()

