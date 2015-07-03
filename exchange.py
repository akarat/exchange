"""
    exchange
    ~~~~~~~~

    Parsing the current exchange rate.

    :copyright: (c) 2015 by Hsiaoming Yang
"""

import re
import requests


__author__ = 'Hsiaoming Yang <me@lepture.com>'
__version__ = '0.1'


def rate(base, target):
    """Get current exchange rate.

    :param base: A base currency
    :param target: Convert to the target currency

    It parses current exchange rate from these services:

        1) Yahoo finance
        2) fixer.io
        3) European Central Bank

    It will fallback to the next service when previous not available.
    The exchane rate is a float number. If `None` is returned, it means
    the parsing goes wrong::

        >>> import exchange
        >>> exchange.rate('USD', 'CNY')
        6.2045
    """
    if base == target:
        return 1.00

    services = [yahoo, fixer, ecb]

    for fn in services:
        try:
            return fn(base, target)
        except:
            pass
    return None


def yahoo(base, target):
    """Parse data from Yahoo."""
    api_url = 'http://finance.yahoo.com/d/quotes.csv'
    resp = requests.get(
        api_url,
        params={
            'e': '.csv',
            'f': 'sl1d1t1',
            's': '{0}{1}=X'.format(base, target)
        },
        timeout=1,
    )
    return resp.content.split(',', 2)[1]


def fixer(base, target):
    """Parse data from fixer.io."""
    api_url = 'http://api.fixer.io/latest'
    resp = requests.get(
        api_url,
        params={
            'base': base,
            'symbols': target,
        },
        timeout=1,
    )
    data = resp.json()
    return data['rates'][target]


def ecb(base, target):
    """Parse data from European Central Bank."""
    api_url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    resp = requests.get(api_url, timeout=1)
    content = resp.content

    def _find_rate(symbol):
        if symbol == 'EUR':
            return 1.00
        m = re.findall(r"currency='%s' rate='([0-9\.]+)'" % symbol, content)
        return float(m[0])

    return round(_find_rate(target) / _find_rate(base), 4)
