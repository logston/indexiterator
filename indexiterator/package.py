from collections import OrderedDict
import json
from urllib.parse import urljoin

import requests

from indexiterator import constants


class PackageDetailsMixin:
    def _get_releases(self):
        releases = self.data.get('releases', {})
        ordered_releases = OrderedDict()
        keys = sorted(releases.keys())
        for key in keys:
            ordered_releases[key] = releases[key]
        return ordered_releases

    def _get_urls(self):
        return self.data.get('urls', [])

    def __getattr__(self, attr):
        if attr in constants.PACKAGE_INFO_KEYS:
            return self.data.get('info', {}).get(attr)
        elif attr == 'releases':
            return self._get_releases()
        elif attr == 'urls':
            return self._get_urls()
        else:
            return super().__getattribute__(attr)


class Package(PackageDetailsMixin):
    def __init__(self, name, index=None):
        self.name = name
        self.index = index
        self._data = None

    def __repr__(self):
        return "<Package '{}'>".format(self.name)

    @property
    def package_url(self):
        if self.index:
            package_url = self.index.package_url
        else:
            package_url = constants.PYPI_PACKAGE_URL

        if not package_url.endswith('/'):
            package_url += '/'

        return urljoin(package_url, self.name)

    @property
    def json_url(self):
        package_url = self.package_url

        if not package_url.endswith('/'):
            package_url += '/'

        return urljoin(package_url, 'json')

    @property
    def data(self):
        if self._data is None:
            data = self._get_json_data()
            self._data = json.loads(data)
        return self._data

    def _get_json_data(self):
        response = requests.get(self.json_url)
        return response.content.decode()

