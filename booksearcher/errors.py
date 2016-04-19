'''
    Exceptions raised and handled in BookSearcher server.
'''


class BookSearcherException(Exception):
    """
         Generic BookSearcher exception
    """
    pass

class ISBNdbException(BookSearcherException):
    """
         ISBNdbException exception
    """
    pass

class ISBNdbServerException(BookSearcherException):
    """
         ISBNdbException exception
    """
    pass