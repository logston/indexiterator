import os
from setuptools import setup

import indexiterator

with open("README.rst") as fd:
    README = fd.read()

with open("LICENSE") as fd:
    LICENSE = fd.read()


setup(
    name='indexiterator',
    version=indexiterator.__version__,
    description='A library for iterating through a PyPI like index.',
    license=LICENSE,
    long_description=README,
    author=indexiterator.__author__,
    author_email=indexiterator.__email__,
    url='https://github.com/logston/indexiterator',
    test_suite='tests',
    keywords=['pypi', 'index', 'package'],
    install_requires=[
        'beautifulsoup4>=4.4.1',
        'ordered-set>=2.0.0',
        'requests>=2.9.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
    ],
)
