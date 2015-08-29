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
        """
        Initialize a new author with series and book inside.
        :return: dict with one author, one series and one book inside
        Example output:
        {
            "author": "Author's Name",
            "series": [
                "series_name": "Some Series",
                "books_in_series": [
                    {
                        "title": "Title of Book",
                        "genres": [
                            "heroic",
                            "fantasy"
                        ]
                    }
                ]
            ]
        }
        """
        result = self.blank_author.copy()
        new_series = self.init_series(series, book)

        result['author'] = author
        result['series'].append(new_series)

        return result

    def init_series(self, series_name, book):
        """ Initialize series dict """
        return {
            "series_name": series_name,
            "books_in_series": [book, ]
        }

    def series_exist(self, series, author):
        """
        Checks whether the given author has the given series
        :return: True, if author has series and False if doesn't
        :return: author_index, which will be used to access authors list
        :return: series_index, if series exist
        """
        i, j = -1, -1
        for i, curr_author in enumerate(self.books):
            if curr_author['author'] == author:
                for j, curr_series in enumerate(curr_author['series']):
                    if curr_series == series:
                        return True, i, j

        return False, i, j

    def format_item(self, item):
        """
        Gather item into properly & pretty formatted dict
        :param item: item to proceed
        """
        author = item['author']

        series = item['series']
        book = dict(title=item['title'], genres=item['genre'], rating=item['average_rating'], votes=item['votes'])

        # Initialize new author
        if author not in self.authors:
            new_author = self.init_author(author, series, book)
            self.books.append(new_author)
            self.authors.append(author)
        else:  # or append current item to existing ones
            series_exist, author_index, series_index = self.series_exist(series, author)
            if series_exist:
                self.books[author_index]['series'][series_index]['books_in_series'].append(book)
            else:
                self.books[author_index]['series'].append(self.init_series(series, book))

    def process_item(self, item, spider):
        self.format_item(dict(item))
        return item

    def close_spider(self, spider):
        # TODO: Make a pagination-like dump to file (to avoid large ones) (probably for 300 items ber *.json file)
        # TODO: Change this method to work directly with django models
        with codecs.open('books.json', 'w', encoding='utf-8') as result_file:
            result_file.write(json.dumps(self.books, indent=4, ensure_ascii=False, sort_keys=True))
