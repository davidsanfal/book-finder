from bookfinder.apis.lirarything_client import LibraryThingClient
import json


class BookInfo(object):

    def __init__(self, data):
        library_things_client = LibraryThingClient()
        title = data.get('title_long')
        self.title = data.get('title') if title == '' else title
        self.isbn13 = data.get('isbn13')
        self.isbn10 = data.get('isbn10')
        publisher = data.get('publisher_text')
        self.publisher = data.get('publisher_name') if publisher == '' else publisher
        author_data = data.get('author_data')
        self.author = author_data[0].get('name') if author_data else 'unknown'
        isbn = self.isbn10 or self.isbn13
        self.cover_url = library_things_client.get_cover_url(isbn)
        self.cover_large_url = library_things_client.get_cover_url(isbn,
                                                                   'large')
        #  Detail Info
        summary = data.get('summary')
        self.summary = 'Book without summary' if summary == '' else summary
        self.language = data.get('language', 'unknown')

    @property
    def to_dict(self):
        return self.__dict__

    @property
    def to_json(self):
        return json.dumps(self.to_dict)


def book_info_to_json(books_info):
    bi = []
    for book in books_info:
        bi.append(book.to_dict)
    return json.dumps(bi)