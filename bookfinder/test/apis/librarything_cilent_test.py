import unittest
from nose_parameterized.parameterized import parameterized
from bookfinder.apis.librarything_client import LibraryThingClient
from bookfinder.errors import LibraryThingException


base_url = 'http://covers.librarything.com/devkey/TEST_API_KEY/{}/isbn/{}'


class LibraryThingClientTest(unittest.TestCase):

    @parameterized.expand([('124578X12D', 'medium', base_url.format('medium', '124578X12D'),
                            None),
                           ('124578X12FCVF', 'large', base_url.format('large', '124578X12FCVF'),
                            None),
                           ('124578X12FCVF', None, base_url.format('medium', '124578X12FCVF'),
                            None),
                           ('124578X12', None, base_url.format('medium', '124578X12'),
                            LibraryThingException),
                           (None, None, base_url.format('medium', '124578X12'),
                            LibraryThingException)])
    def get_cover_test(self, isbn, size, result, raised):
        client = LibraryThingClient()
        client.api_key = 'TEST_API_KEY'
        if raised:
            self.assertRaises(LibraryThingException, client.get_cover_url, isbn, size)
        elif size:
            url = client.get_cover_url(isbn, size)
            self.assertEqual(url, result)
        else:
            url = client.get_cover_url(isbn)
            self.assertEqual(url, result)

if __name__ == '__main__':
    unittest.main()
