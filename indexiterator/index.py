from bs4 import BeautifulSoup
from ordered_set import OrderedSet
import requests

from indexiterator import constants
from indexiterator.package import Package


class Index:
    def __init__(self,
                 simple_url=constants.PYPI_SIMPLE_URL,
                 package_url=constants.PYPI_PACKAGE_URL):
        self.package_url = package_url
        self.simple_url = simple_url
        self._package_names = None

    @property
    def package_names(self):
        if self._package_names is None:
            self._package_names = OrderedSet()
            self.reload()

        return self._package_names

    def _get_html_data(self):
        if self.simple_url.startswith('/'):
            with open(self.simple_url) as fp:
                data = fp.read()
        else:
            response = requests.get(self.simple_url)
            data = response.content

        return data
 
    def _get_names(self):
        data = self._get_html_data()
        soup = BeautifulSoup(data, 'html.parser')
        links = soup.find_all('a')
        names = (link.string for link in links)
        return names

    def _add_package_names(self, names):
        if self._package_names is None:
            self._package_names = OrderedSet()
 
        for name in names:
            self._package_names.add(name)

    def reload(self):
        """
        Reload package names from index.
        """
        names = self._get_names()
        self._add_package_names(names)

    def __len__(self):
        if self._package_names is None:
            return 0
        return len(self.package_names)

    def __iter__(self):
        return (Package(name, self) for name in self.package_names)

    def __repr__(self):
        return "<Index '{}'>".format(self.simple_url)

