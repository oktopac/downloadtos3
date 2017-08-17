import unittest
import handler

class TestCreateS3Key(unittest.TestCase):

    def test_creates1(self):
        web_location = "http://www.google.com/test/baa.html?cdscds+"
        s3_location = None
        key = handler.create_s3_key(web_location, s3_location)
        self.assertEqual("baa.html", key)

    def test_creates2(self):
        web_location = "http://www.google.com/test/baa.html?cdscds+"
        s3_location = '/'
        key = handler.create_s3_key(web_location, s3_location)
        self.assertEqual("baa.html", key)

    def test_creates3(self):
        web_location = "http://www.google.com/test/baa.html?cdscds+"
        s3_location = '/fdsfds'
        key = handler.create_s3_key(web_location, s3_location)
        self.assertEqual("/fdsfds/baa.html", key)

    def test_creates4(self):
        web_location = "http://www.google.com/test/baa.html?cdscds+"
        s3_location = '/fdsfds/'
        key = handler.create_s3_key(web_location, s3_location)
        self.assertEqual("/fdsfds/baa.html", key)

    def test_creates5(self):
        web_location = "http://www.google.com/test/baa.html?cdscds+"
        s3_location = '/fdsfds/dssacascasxas'
        key = handler.create_s3_key(web_location, s3_location)
        self.assertEqual("/fdsfds/dssacascasxas/baa.html", key)

if __name__ == '__main__':
    unittest.main()
