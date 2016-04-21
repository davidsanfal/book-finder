import unittest
from bookfinder.server.services.book_service import BookService
from mock.mock import MagicMock
from nose_parameterized.parameterized import parameterized
from bookfinder.errors import BookSearcherException,\
    BookSearcherMaxPageException
from bookfinder.test.utils.output_utils import clean_code_quert_01, jhon_queary_1


class BookServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = BookService()

    @parameterized.expand([({'data': {}, 'text': 'd'}, 'q', 'all', 1, BookSearcherException),
                           (clean_code_quert_01, 'q', 'all', 1, None),
                           (jhon_queary_1, 'q', 'all', 1, None),
                           (jhon_queary_1, 'q', 'all', 11, None),
                           (jhon_queary_1, 'q', 'all', 12, BookSearcherMaxPageException)])
    def search_test(self, output, query, query_type, page, raised):
        self.service.isbndb_client.search = MagicMock(side_effect=self.search_mock(output))
        if raised:
            self.assertRaises(raised, self.service.serch, query, query_type, page)
        else:
            self.service.serch(query, query_type, page)

    def search_mock(self, output):
        def side_effect(query, query_type, page):
            return output
        return side_effect

if __name__ == '__main__':
    unittest.main()
