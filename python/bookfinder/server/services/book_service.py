from bookfinder.apis.isbndb_client import ISBNdbClient
from bookfinder.errors import ISBNdbException, BookSearcherException,\
    BookSearcherMaxPageException
from bookfinder.server.models.book_model import BookInfo


class BookService(object):

    def __init__(self):
        self.isbndb_client = ISBNdbClient()

    def serch(self, query, query_type, page=1):
        books_info = []
        try:
            json_info = self.isbndb_client.search(query,
                                                  query_type,
                                                  page)
        except ISBNdbException as e:
            raise BookSearcherException(e.message)
        max_page = json_info.get('page_count')
        if max_page and max_page < page:
            raise BookSearcherMaxPageException()
        if not json_info['data']:
            error_message = 'Unable to locate any book with "%s"' % query
            raise BookSearcherException(error_message)
        for data in json_info['data']:
            books_info.append(BookInfo(data))
        return books_info, max_page
