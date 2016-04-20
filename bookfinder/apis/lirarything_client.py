import os
from bookfinder.environment import LIBRARYTHING_API_KEY


class LibraryThingClient(object):

    def __init__(self):
        self.api_key = LIBRARYTHING_API_KEY
        self.base_url = 'http://covers.librarything.com/devkey/{}/{}/isbn/{}'

    def get_cover_url(self, isbn, size='medium'):
        if isbn:
            return self.base_url.format(self.api_key,
                                        size,
                                        isbn)
