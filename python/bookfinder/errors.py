'''
    Exceptions raised and handled in BookSearcher server.
'''


class BookSearcherException(Exception):
    """
         Generic BookSearcher exception
    """
    pass


class BookSearcherMaxPageException(BookSearcherException):
    """
         MaxPage BookSearcher exception
    """
    pass


class EnvironmentException(Exception):
    """
         Environment exception
    """
    pass


class ISBNdbException(BookSearcherException):
    """
         ISBNdbClient exception
    """
    pass


class LibraryThingException(BookSearcherException):
    """
         LibraryThingClient exception
    """
    pass


class ISBNdbServerException(BookSearcherException):
    """
         ISBNdbException exception
    """
    pass
