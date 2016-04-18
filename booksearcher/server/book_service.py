from booksearcher.apis.isbndb_client import ISBNdbClient


class BookService(object):

    def __init__(self):
        self.isbndb_client = ISBNdbClient()

    def serch(self, book_info):
        return None