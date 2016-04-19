from booksearcher.apis.isbndb_client import ISBNdbClient
from booksearcher.errors import ISBNdbException, BookSearcherException
import json
from booksearcher.apis.lirarything_client import LibraryThingClient


class BookInfo(object):

    def __init__(self, data):
        library_things_client = LibraryThingClient()
        self.title = data.get('title')
        self.isbn13 = data.get('isbn13')
        self.isbn10 = data.get('isbn10')
        self.publisher = data.get('publisher_name')
        author_data = data.get('author_data')
        self.author = author_data[0].get('name') if author_data else 'unknown'
        isbn = self.isbn10 or self.isbn13
        self.cover_url = library_things_client.get_cover_url(isbn)

    @property
    def to_dict(self):
        return self.__dict__


class BookService(object):

    def __init__(self):
        self.isbndb_client = ISBNdbClient()

    def serch(self, query, query_type):
        query_type = None if query_type == 'partial_title' else query_type
        books_info = []
        try:
            json_info = self.isbndb_client.search(query, query_type)
        except ISBNdbException as e:
            raise BookSearcherException(e.message)
        if not json_info['data']:
            raise BookSearcherException('0 books')
        for data in json_info['data']:
            books_info.append(BookInfo(data).to_dict)
        return json.dumps(books_info)
