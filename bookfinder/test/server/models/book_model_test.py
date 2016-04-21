import unittest
from bookfinder.test.utils.output_utils import clean_code_quert_01
from bookfinder.server.models.book_model import BookInfo


class BookInfoTest(unittest.TestCase):

    def book_info_test(self):
        output = {'publisher': u'Indianapolis, Ind. : Prentice Hall ; c2009.',
                  'isbn10': u'0132350882',
                  'isbn13': u'9780132350884',
                  'author': u'Martin, Robert W. T.',
                  'title': u'Clean code: a handbook of agile software craftsmanship',
                  'summary': 'Book without summary',
                  'language': u'eng'}
        result = BookInfo(clean_code_quert_01['data'][0]).to_dict
        for key, value in output.iteritems():
            self.assertEqual(value, result[key])

if __name__ == '__main__':
    unittest.main()
