import unittest
from bookfinder.server.app import finder_app
from bookfinder.environment import SECRET_APP_KEY


class FinderAppTestCase(unittest.TestCase):

    def setUp(self):
        finder_app.app.config['TESTING'] = True
        self.app = finder_app.app.test_client()

    def test_config(self):
        self.assertTrue(self.app.application.config['WTF_CSRF_ENABLED'])
        self.assertEqual(self.app.application.config['SECRET_KEY'], SECRET_APP_KEY)
        self.assertTrue(self.app.application.config['BOOTSTRAP_QUERYSTRING_REVVING'])
        self.assertFalse(self.app.application.config['BOOTSTRAP_LOCAL_SUBDOMAIN'])
        self.assertTrue(self.app.application.config['BOOTSTRAP_USE_MINIFIED'])

if __name__ == '__main__':
    unittest.main()
