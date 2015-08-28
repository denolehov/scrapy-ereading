# -*- coding: utf-8 -*-
import scrapy

from ereading.utilites import get_url
from ereading.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["e-reading.club"]
    start_urls = (
        'http://www.e-reading.club/',
    )

    def get_value(self, xpath):
        result = xpath.extract()
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            return result
        else:
            return "None"

    def parse(self, response):
        self.logger.info('Parse starting for %s' % response.url)

        for link in response.xpath('//div/nofollow/a/@href').extract():
            if link.startswith('/author'):
                yield scrapy.Request(url=get_url(response, link), callback=self.parse_list_of_authors)

    def parse_list_of_authors(self, response):
        for link in response.xpath('//tr/td/a/@href').extract():
            if link.startswith('bookbyauthor'):
                yield scrapy.Request(url=get_url(response, link), callback=self.parse_authors_page)

    def parse_authors_page(self, response):
        for link in response.xpath('//*[@class="bookrecord"]/a/@href').extract():
            yield scrapy.Request(url=get_url(response, link), callback=self.parse_book)

    def parse_book(self, response):
        title = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "bookreader")]/text()'))
        author = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "bookbyauthor")]/strong/text()'))
        series = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "series")]/text()'))
        average_rating = self.get_value(response.xpath('//span[@itemprop="average"]/text()'))
        votes = self.get_value(response.xpath('//span[@itemprop="votes"]/text()'))
        genre = self.get_value(response.xpath('//table/tr/td/a[@itemprop="category genre"]/text()'))

        yield BookItem(title=title, author=author, average_rating=average_rating, votes=votes, series=series,
                       genre=genre)
