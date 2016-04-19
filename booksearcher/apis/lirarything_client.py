import os


class LibraryThingClient(object):

    def __init__(self):
        self.api_key = os.environ.get('LIBRARYTHING_API_KEY')
        self.base_url = 'http://covers.librarything.com/devkey/%s/medium/isbn/' % self.api_key

    def get_cover_url(self, isbn=None):
        if isbn:
            return self.base_url + isbn
