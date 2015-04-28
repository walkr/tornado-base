import os
import sys
import unittest

from webtest import WebTestCase

sys.path.append(os.path.dirname(__file__) + '/..')


class HTTPTest(WebTestCase):

    def test_get_main(self):
        for url in ['/', '/about', '/term', '/privacy', 'signup', 'login']:
            resp = self.fetch('/')
            self.assertEqual(200, resp.code)

    def test_get_users(self):
        resp = self.fetch('/v1/users')
        self.assertEqual(200, resp.code)

    def test_get_comments(self):
        resp = self.fetch('/v1/comments')
        self.assertEqual(200, resp.code)


if __name__ == '__main__':
    unittest.main()
