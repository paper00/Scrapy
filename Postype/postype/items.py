# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PostypeItem(scrapy.Item):
    # define the fields for your item here like:
    post_category = scrapy.Field()
    post_title = scrapy.Field()
    post_subtitle = scrapy.Field()
    author = scrapy.Field()
    post_content = scrapy.Field()

