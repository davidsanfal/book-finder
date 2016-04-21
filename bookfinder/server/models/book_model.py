from bookfinder.apis.lirarything_client import LibraryThingClient
import json


class BookInfo(object):
    '''Book info container, this class receives a dict with all the book info and
       extracts the important information to render in the book profile'''

    def __init__(self, data):
        library_things_client = LibraryThingClient()
        self.title = self.retrieve(data, 'title_long', data.get('title'))
        self.isbn13 = data.get('isbn13')
        self.isbn10 = data.get('isbn10')
        _publisher = data.get('publisher_text')
        self.retrieve(data, 'publisher_text', data.get('publisher_name'))
        _publisher = self.retrieve(data, 'publisher_text', data.get('publisher_name'))
        self.publisher = 'unknown' if _publisher == '' else _publisher
        _author_data = data.get('author_data')
        self.author = _author_data[0].get('name') if _author_data else 'unknown'
        _isbn = self.isbn10 or self.isbn13
        self.cover_url = library_things_client.get_cover_url(_isbn)
        self.cover_large_url = library_things_client.get_cover_url(_isbn, 'large')
        #  Detail Info
        self.retrieve(data, 'summary', 'Book without summary')
        self.summary = self.retrieve(data, 'summary', 'Book without summary')
        self.language = self.retrieve(data, 'language', 'unknown')

    @staticmethod
    def retrieve(data, value, default):
        '''Utility function to retrive some information from data'''
        return default if data.get(value) == '' else data.get(value)

    @property
    def to_dict(self):
        '''return a BookInfo dict summary'''
        return self.__dict__

    @property
    def to_json(self):
        '''return a BookInfo josn summary'''
        return json.dumps(self.to_dict)


def book_info_to_json(books_info, pages):
    '''Utility function, recives a list of books and generates a json dict'''
    bi = []
    for book in books_info:
        bi.append(book.to_dict)
    return json.dumps({'books': bi,
                       'pages': pages})
