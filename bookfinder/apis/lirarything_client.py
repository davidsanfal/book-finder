from bookfinder.environment import LIBRARYTHING_API_KEY
from bookfinder.errors import LibraryThingException


class LibraryThingClient(object):
    '''Minimal client to build a url book cover'''

    def __init__(self):
        self.api_key = LIBRARYTHING_API_KEY
        self.base_url = 'http://covers.librarything.com/devkey/{}/{}/isbn/{}'

    def get_cover_url(self, isbn, size='medium'):
        '''Returns the cover with the ISBN specified'''
        if isbn and self.correct_isbn(isbn):
            return self.base_url.format(self.api_key,
                                        size,
                                        isbn)
        else:
            raise LibraryThingException('ISBN required')

    @staticmethod
    def correct_isbn(isbn):
        '''Utility function to check if the isbn number is correct'''
        return len(isbn) in (10, 13)
