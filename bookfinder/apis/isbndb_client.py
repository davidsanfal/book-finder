import requests
import os
import json
import re
from bookfinder.errors import ISBNdbException, ISBNdbServerException


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

TITLE_SEARCH = 'title'
ISBN_SEARCH = 'isbn'


class ISBNdbClient(object):

    def __init__(self):
        self.api_key = os.environ.get('ISBNDB_API_KEY')
        self.base_url = 'http://isbndb.com/api/v2/json/%s' % self.api_key

    def request(self, request_info):
        url = self.base_url + request_info  # '/book/084930315X'
        response = requests.get(url=url)
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

    def get_books(self, info, index=None):
        info = urlify(info)
        request_url = '/books/?q=%s' % info
        if index:
            if index in INDEX_PARAMETERS:
                request_url = request_url + '&i=%s' % index
            else:
                raise ISBNdbException()
        return self.request(request_url)

    def search(self, info, query_type):
        if query_type == ISBN_SEARCH:
            return self.get_book(info)
        elif query_type == TITLE_SEARCH:
            try:
                return self.get_book(info)
            except ISBNdbException:
                query_type = None
        return self.get_books(info, query_type)
