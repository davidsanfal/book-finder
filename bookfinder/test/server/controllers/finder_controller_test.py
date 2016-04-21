import unittest
from bookfinder.server.app import finder_app
from bookfinder.server.controllers import finder_controller
from bookfinder.server.controllers import book_controller


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        finder_app.app.config['TESTING'] = True
        self.app = finder_app.app.test_client()

    def tearDown(self):
        pass

    def test_finder(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()
