Index Iterator
==============

A library for iterating through a PyPI like index

::

    from indexiterator import Index

    index = Index()  # defaults to using PyPI index

    for pacakge in index:
        # do something with package

