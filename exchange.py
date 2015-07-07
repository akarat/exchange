"""
    exchange
    ~~~~~~~~

    Parsing the current exchange rate.

    :copyright: (c) 2015 by Hsiaoming Yang
"""

import re
import decimal
import logging
import requests


__author__ = 'Hsiaoming Yang <me@lepture.com>'
__version__ = '0.3'

__all__ = ['rate']

logger = logging.getLogger('exchange')


def rate(base, target, error_log=None):
    """Get current exchange rate.

    :param base: A base currency
    :param target: Convert to the target currency
    :param error_log: A callable function to track the exception

    It parses current exchange rate from these services:

        1) Yahoo finance
        2) fixer.io
        3) European Central Bank

    It will fallback to the next service when previous not available.
    The exchane rate is a decimal number. If `None` is returned, it means
    the parsing goes wrong::

        >>> import exchange
        >>> exchange.rate('USD', 'CNY')
        Decimal('6.2045')
    """
    if base == target:
        return decimal.Decimal(1.00)

    services = [yahoo, fixer, ecb]
    if error_log is None:
        error_log = _error_log

    for fn in services:
        try:
            return fn(base, target)
        except Exception as e:
            error_log(e)
    return None


def _error_log(e):
    logger.exception('Exchange Exception: %r' % e)


def yahoo(base, target):
    """Parse data from Yahoo."""
    api_url = 'http://download.finance.yahoo.com/d/quotes.csv'
    resp = requests.get(
        api_url,
        params={
            'e': '.csv',
            'f': 'sl1d1t1',
            's': '{0}{1}=X'.format(base, target)
        },
        timeout=1,
    )
    value = resp.text.split(',', 2)[1]
    return decimal.Decimal(value)


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
    return decimal.Decimal(data['rates'][target])


def ecb(base, target):
    """Parse data from European Central Bank."""
    api_url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    resp = requests.get(api_url, timeout=1)
    text = resp.text

    def _find_rate(symbol):
        if symbol == 'EUR':
            return decimal.Decimal(1.00)
        m = re.findall(r"currency='%s' rate='([0-9\.]+)'" % symbol, text)
        return decimal.Decimal(m[0])

    return _find_rate(target) / _find_rate(base)
