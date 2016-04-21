import unittest
from bookfinder.apis.isbndb_client import ISBNdbClient
from mock.mock import MagicMock
from nose_parameterized.parameterized import parameterized
from bookfinder.errors import ISBNdbException
from bookfinder.test.utils.output_utils import jhon_queary_1, \
                                              clean_code_quert_01


def side_effect(request_info):
    return request_info


class ISBNdbClientTest(unittest.TestCase):

    @parameterized.expand([('124578X12', '/book/124578X12'),
                           ('one book', '/book/one_book'),
                           ('I can\'t get no satisfaction!',
                            '/book/I_cant_get_no_satisfaction')])
    def simple_get_book_test(self, query, result):
        client = ISBNdbClient()
        client.request = MagicMock(side_effect=side_effect)
        request_value = client.get_book(query)
        self.assertEqual(request_value, result)

    @parameterized.expand([('clean code', {}, ISBNdbException),
                           ('clean code: a handbook of agile software craftsmanship',
                            clean_code_quert_01, None)])
    def real_get_book_test(self, query, result, raised):
        client = ISBNdbClient()
        if raised:
            self.assertRaises(raised, client.get_book, query)
        else:
            request_value = client.get_book(query)
            self.assertEqual(request_value, result)

    @parameterized.expand([('jhon rambo', None, 1,
                            '/books?q=jhon_rambo&p=1', None),
                           ('jhon rambo', 'legs', 3,
                            None, ISBNdbException),
                           ('jhon rambo', 'book_summary', 3,
                            '/books?q=jhon_rambo&i=book_summary&p=3', None)])
    def simple_get_books_test(self, query, index, page, result, raised):
        client = ISBNdbClient()
        client.request = MagicMock(side_effect=side_effect)
        if raised:
            self.assertRaises(raised, client.get_books, query, index, page)
        else:
            request_value = client.get_books(query, index, page)
            self.assertEqual(request_value, result)

    @parameterized.expand([('jhon rambo', 'legs', 3,
                            None, ISBNdbException),
                           ('jhon rambo', 'book_summary', 3,
                            jhon_queary_1, None)])
    def real_get_books_test(self, query, index, page, result, raised):
        client = ISBNdbClient()
        if raised:
            self.assertRaises(raised, client.get_books, query, index, page)
        else:
            request_value = client.get_books(query, index, page)
            self.assertEqual(request_value, result)

    @parameterized.expand([('clean code', 'title', 1, None, ISBNdbException),
                           ('clean code: a handbook of agile software craftsmanship',
                            'title', 1, clean_code_quert_01, None),
                           ('jhon rambo', 'legs', 3,
                            None, ISBNdbException),
                           ('jhon rambo', 'book_summary', 3,
                            jhon_queary_1, None)])
    def search_test(self, query, index, page, result, raised):
        client = ISBNdbClient()
        if raised:
            self.assertRaises(raised, client.search, query, index, page)
        else:
            request_value = client.search(query, index, page)
            self.assertEqual(request_value, result)

if __name__ == '__main__':
    unittest.main()
