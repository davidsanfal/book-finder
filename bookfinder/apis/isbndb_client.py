import requests
import json
import re
from bookfinder.errors import ISBNdbException, ISBNdbServerException
from requests.exceptions import ConnectionError, Timeout, RequestException
from bookfinder.environment import ISBNDB_API_KEY


def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single underscore
    s = re.sub(r"\s+", '_', s)
    return s


INDEX_PARAMETERS = ['author_id',  # (ISBNdb's internal author_id)
                    'author_name',
                    'publisher_id',  # (ISBNdb's internal publisher_id)
                    'publisher_name',
                    'book_summary',
                    'book_notes',
                    'dewey',  # (dewey decimal number)
                    'lcc',  # (library of congress number)
                    'combined',  # (searches across title, author name and publisher name)
                    'full',  # (searches across all indexes)
                    ]

INDEX_SIMPLE_SEARCH = ['title',  # (searches a specific title book)
                       'isbn',  # (searches a specific isbn book)
                       ]

INDEX_ALL_BOOKS = 'all'  # (searches across all books)


class ISBNdbClient(object):

    def __init__(self):
        self.api_key = ISBNDB_API_KEY
        self.base_url = 'http://isbndb.com/api/v2/json/%s' % self.api_key

    def request(self, request_info):
        url = self.base_url + request_info  # '/book/084930315X'
        try:
            response = requests.get(url=url)
        except Timeout:
            raise ISBNdbServerException('ISBNdb server timed out')
        except ConnectionError:
            raise ISBNdbServerException('Connection error')
        except RequestException as e:
            raise ISBNdbServerException('ISBNdb server error: %s' % e)
        if response.status_code != 200:
            raise ISBNdbServerException('ISBNdb response error')
        data = json.loads(response.content)
        error = data.get('error')
        if error:
            raise ISBNdbException(error)
        return data

    def get_book(self, info):
        info = urlify(info)
        return self.request('/book/%s' % info)

    def get_books(self, info, index=None, page=1):
        info = urlify(info)
        request_url = '/books?q=%s' % info
        if index:
            if index in INDEX_PARAMETERS:
                request_url = request_url + '&i=%s' % index
            else:
                raise ISBNdbException('Invalid query index: %s' % index)
        request_url = request_url + '&p=%s' % page
        return self.request(request_url)

    def search(self, info, query_type, page):
        if query_type in INDEX_SIMPLE_SEARCH:
            return self.get_book(info)
        query_type = None if query_type == INDEX_ALL_BOOKS else query_type
        return self.get_books(info, query_type, page)
