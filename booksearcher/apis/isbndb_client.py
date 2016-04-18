import requests
import os
import json
import re


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


class ISBNdbClient(object):

    def __init__(self):
        self.api_key = os.environ.get('ISBNDB_API_KEY')
        self.base_url = 'http://isbndb.com/api/v2/json/%s' % self.api_key

    def request(self, request_info):
        url = self.base_url + request_info  # '/book/084930315X'
        response = requests.get(url=url)
        if response.status_code != 200:
            raise Exception('ISBN ERROR')
        data = json.loads(response.content)
        return data

    def get_book(self, info):
        info = urlify(info)
        return self.request('/book/%s' % info)

    def get_books(self, info, index=None):
        info = urlify(info)
        request_url = '/books/?q=%s' % info
        if index and index in INDEX_PARAMETERS:
            request_url = request_url + '&i=%s' % index
        print request_url
        return self.request(request_url)

# client = ISBNdbClient()
# print client.get_book('principles of solid mechanics')
# print client.get_books('john', 'author_name')
