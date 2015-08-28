# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    average_rating = scrapy.Field()
    votes = scrapy.Field()
    series = scrapy.Field()
    genre = scrapy.Field()
    # description = scrapy.Field()
