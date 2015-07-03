Exchange Rate
=============

Get current exchange rate.

It parses current exchange rate from these services:

* Yahoo finance
* fixer.io
* European Central Bank

Installation
------------

Using pip to install it::

    $ pip install exchange

Usage
-----

The only method you would use is ``rate``::

    >>> import exchange
    >>> exchange.rate('USD', 'CNY')

License
-------

This project is licensed with BSD. See LICENSE for more detail.
