import unittest
from bookfinder.server.app import finder_app
from bookfinder.server.controllers import finder_controller
from bookfinder.server.controllers import book_controller
from nose_parameterized.parameterized import parameterized


class BookControllerTestCase(unittest.TestCase):

    def setUp(self):
        finder_app.app.config['TESTING'] = True
        self.app = finder_app.app.test_client()

    @parameterized.expand([('0132350882', 200),
                           ('0132350002', 302)])
    def test_book(self, isbn, status):
        rv = self.app.get('book/%s' % isbn, follow_redirects=False)
        self.assertEqual(rv.status_code, status)

    @parameterized.expand([(1, 'all', 'clean+code', 200),
                           (1, 'all', 'asdqwe', 302),
                           (1857, 'all', 'asdqwe', 302),
                           (1857, 'all', 'clean+code', 404)])
    def test_books(self, page, q_type, q_data, status):
        route = self.books_route(page, q_type, q_data)
        rv = self.app.get(route, follow_redirects=False)
        self.assertEqual(rv.status_code, status)

    def books_route(self, page, q_type, q_data):
        route = '/books/{}?query=%7B"type"%3A+"{}"%2C+"data"%3A+"{}"%7D'
        return route.format(page, q_type, q_data)

if __name__ == '__main__':
    unittest.main()
