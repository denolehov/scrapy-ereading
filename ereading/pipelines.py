# -*- coding: utf-8 -*-
import json
import codecs


class BookPipeline(object):

    def __init__(self):
        self.books = []
        self.authors = []
        self.blank_author = {
            "author": '',
            "series": []
        }

    def init_author(self, author, series, book):
        result = self.blank_author.copy()

        new_series = self.init_series(series, book)

        result['author'] = author
        result['series'].append(new_series)

        return result

    def init_series(self, series_name, book):
        return {
            "serie_name": series_name,
            "books_in_series": [book, ]
        }

    def series_exist(self, series, author):
        i, j = -1, -1
        for i, curr_author in enumerate(self.books):
            if curr_author['author'] == author:
                for j, curr_series in enumerate(curr_author['series']):
                    if curr_series == series:
                        return True, i, j

        return False, i, j

    def format_item(self, item):
        author = item['author']

        series = item['series']
        book = dict(title=item['title'], genres=item['genre'], rating=item['average_rating'], votes=item['votes'])

        if author not in self.authors:
            new_author = self.init_author(author, series, book)
            self.books.append(new_author)
            self.authors.append(author)
        else:
            series_exist, author_index, series_index = self.series_exist(series, author)
            if series_exist:
                self.books[author_index]['series'][series_index]['books_in_series'].append(book)
            else:
                self.books[author_index]['series'].append(self.init_series(series, book))

    def process_item(self, item, spider):
        self.format_item(dict(item))
        return item

    def close_spider(self, spider):
        result_file = codecs.open('books.json', 'w', encoding='utf-8')
        result_file.write(json.dumps(self.books, indent=4, ensure_ascii=False, sort_keys=True))
        result_file.close()
