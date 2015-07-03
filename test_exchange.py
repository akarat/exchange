import exchange


def test_rate():
    rate = exchange.rate('USD', 'CNY')
    assert rate > 6
    assert rate < 7


def test_rate_is_none():
    rate = exchange.rate('USD', 'INVID')
    assert rate is None


def test_rate_is_1():
    assert exchange.rate('USD', 'USD') == 1.00


def test_yahoo():
    rate = exchange.yahoo('USD', 'CNY')
    assert rate > 6
    assert rate < 7


def test_fixer():
    rate = exchange.fixer('USD', 'CNY')
    assert rate > 6
    assert rate < 7


def test_ecb():
    rate = exchange.ecb('USD', 'CNY')
    assert rate > 6
    assert rate < 7


def test_ecb_eur():
    rate = exchange.ecb('EUR', 'EUR')
    assert rate == 1.00
