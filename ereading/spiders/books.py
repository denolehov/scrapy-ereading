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
        """
        Created to reformat:
            ["Some Example"] -> "Some Example" (or "None" if no data in xpath)
        :param xpath: raw xpath to extract data from
        """
        result = xpath.extract()
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            return result
        else:
            return "None"

    def parse(self, response):
        """
        At this point we go through alphabet and
        yielding Requests to pages with list of authors
        """
        for link in response.xpath('//div/nofollow/a/@href').extract():
            if link.startswith('/author'):
                yield scrapy.Request(url=get_url(response, link), callback=self.parse_list_of_authors)

    def parse_list_of_authors(self, response):
        """ Here we follow all the authors links """
        for link in response.xpath('//tr/td/a/@href').extract():
            if link.startswith('bookbyauthor'):
                yield scrapy.Request(url=get_url(response, link), callback=self.parse_authors_page)

    def parse_authors_page(self, response):
        """ Follow all the book-detail urls """
        for link in response.xpath('//*[@class="bookrecord"]/a/@href').extract():
            yield scrapy.Request(url=get_url(response, link), callback=self.parse_book)

    def parse_book(self, response):
        """
        Parse the title, author, series etc. of the book.
        If we get no data from parse output, assign "None" to several field.
        """
        # TODO: Debug title (and possibly other fields (xpaths)) because it gives "None" too often
        title = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "bookreader")]/text()'))
        author = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "bookbyauthor")]/strong/text()'))
        series = self.get_value(response.xpath('//table/tr/td/a[contains(@href, "series")]/text()'))
        average_rating = self.get_value(response.xpath('//span[@itemprop="average"]/text()'))
        votes = self.get_value(response.xpath('//span[@itemprop="votes"]/text()'))
        genre = response.xpath('//table/tr/td/a[@itemprop="category genre"]/text()').extract()

        yield BookItem(title=title, author=author, average_rating=average_rating, votes=votes, series=series,
                       genre=genre)
