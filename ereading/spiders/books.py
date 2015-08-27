# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["e-reading.club"]
    start_urls = (
        'http://www.e-reading.club/',
    )

    def parse(self, response):
        pass
