import os
import riceuber
import unittest
import tempfile

class RiceUberTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, RiceUber.app.config['DATABASE'] = tempfile.mkstemp()
        RiceUber.app.config['TESTING'] = True
        self.app = RiceUber.app.test_client()
        RiceUber.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(RiceUber.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()