import json
import os
import unittest
from unittest.mock import patch

from indexiterator import Index, Package


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


class TestPackage(unittest.TestCase):
    def test_urls(self):
        p = Package('catzzz')
        self.assertEqual(p.package_url, 'https://pypi.python.org/pypi/catzzz')
        self.assertEqual(p.json_url, 'https://pypi.python.org/pypi/catzzz/json')

    def test_data(self):
        return_value = '{"info":{"maintainer": null, "release_url": "http://..."}}'

        with patch.object(Package, '_get_json_data', return_value=return_value):
            p = Package('fake-paul-package')
            result = p.data
            expected = json.loads(return_value)
            self.assertEqual(result, expected)


class TestPackageDetailsMixin(unittest.TestCase):
    def test_info(self):
        _data = {
            "info": {
                "maintainer": "Paul",
                "release_url": "http://..."
            }
        }

        p = Package('fake-paul-package')
        p._data = _data
        self.assertEqual(p.maintainer, "Paul")

    def test_info(self):
        _data = {
            "releases": {
                "0.1.0": [
                    {
                        "has_sig": False,
                        "upload_time": "2014-11-23T14:42:44",
                        "comment_text": "",
                        "python_version": "source",
                        "url": "https://.../catzzz/catzzz-0.1.0.tar.gz",
                        "md5_digest": "a7673b40a5abb553e0a9f05dbb9e5ea5",
                        "downloads": 1255,
                        "filename": "catzzz-0.1.0.tar.gz",
                        "packagetype": "sdist",
                        "path": "source/c/catzzz/catzzz-0.1.0.tar.gz",
                        "size": 2479
                    }
                ],
            }
        }

        p = Package('fake-paul-package')
        p._data = _data

        releases = _data.get('releases')

        self.assertEqual(p.releases, releases)




