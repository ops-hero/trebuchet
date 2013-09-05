import os
import unittest
import tempfile

from main import app as my_app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.client = my_app.test_client()
        
    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.client.get('/')
        assert 'Hello World!' in rv.data

if __name__ == '__main__':
    unittest.main()