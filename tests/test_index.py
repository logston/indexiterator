import os
import unittest

from indexiterator import Index


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, 'data')


class TestIndex(unittest.TestCase):
    def test_reload(self):
        path = os.path.join(DATA_DIR, 'simple.html')
        # Make sure we don't hit the real PyPI
        self.assertTrue(path.startswith('/'))

        index = Index(path)
        self.assertEqual(len(index), 0)
        index.reload()
        self.assertEqual(len(index), 72931)



