from datetime import datetime
import json
import os
import unittest
from unittest.mock import patch

from indexiterator import Package
from indexiterator.package import min_upload_time


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, 'data')


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

    def test_releases_in_order(self):
        p = Package('numpy')
        with open(os.path.join(DATA_DIR, 'numpy.json')) as fp:
            data = json.load(fp)
        p._data = data

        result = list(p.releases.keys())
        expected = ['1.0', '1.3.0', '1.4.1', '1.5.0', '1.5.1', '1.6.0',
                    '1.6.1', '1.6.2', '1.7.0', '1.7.1', '1.8.0', '1.7.2',
                    '1.8.1', '1.8.2', '1.9.0', '1.9.1', '1.9.2', '1.9.3',
                    '1.10.0', '1.10.1', '1.10.2', '1.10.4']
        self.assertEqual(result, expected)


class TestUtils(unittest.TestCase):

    def test_min_upload_time(self):
        with open(os.path.join(DATA_DIR, 'numpy.json')) as fp:
            data = json.load(fp)

        releases = data.get('releases')

        result = min_upload_time('1.10.4', releases)
        expected = datetime(2016, 1, 7, 2, 41, 56)
        self.assertEqual(result, expected)

