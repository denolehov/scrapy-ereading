# -*- coding: utf-8 -*-
import json
import codecs


class BookPipeline(object):

    def __init__(self):
        self.books = []

    def process_item(self, item, spider):
        self.books.append(dict(item))
        return item

    def close_spider(self, spider):
        result_file = codecs.open('books.json', 'w', encoding='utf-8')
        result_file.write(json.dumps(self.books, indent=4, ensure_ascii=False, sort_keys=True))
        result_file.close()
