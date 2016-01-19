from collections import OrderedDict
from datetime import datetime
import json
from urllib.parse import urljoin

import requests

from indexiterator import constants


def min_upload_time(key, releases):
    release_list = releases.get(key)
    min_ts = None
    for release in release_list:
        upload_dt_str = release.get('upload_time')
        dt_format = '%Y-%m-%dT%H:%M:%S'

        try:
            upload_dt = datetime.strptime(upload_dt_str, dt_format)
        except ValueError:
            continue

        if min_ts is None or upload_dt < min_ts:
            min_ts = upload_dt

    return min_ts


class PackageDetailsMixin:
    def _get_releases(self):
        releases = self.data.get('releases', {})
        ordered_releases = OrderedDict()
        keys = (key for key, value in releases.items() if value)
        keys = sorted(keys, key=lambda key: min_upload_time(key, releases))
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

    def __iter__(self):
        return (Release(version, self) for version in self.releases)


class Release:

    def __init__(self, version, package):
        self.version = version
        self.package = package

    def get_tarball(self):
        release_list = self.package.releases.get(self.version)
        for release in release_list:
            if release.get('url', '').endswith('.tar.gz'):
                break

        if not release:
            return

        url = release.get('url')
        response = requests.get(url)

        return response.content

    def __repr__(self):
        return "<Release '{}:{}'>".format(self.package.name, self.version)

