from collections import namedtuple
import datetime
from decimal import Decimal as D

from django.conf import settings

from exchange.adapters import BaseAdapter
from exchange.utils import import_class
from exchange.models import ExchangeRate
from exchange.cache import (update_rates_cached, get_rate_cached,
                            get_rates_cached, CACHE_ENABLED)
from moneyed import Money


EXCHANGE_ADAPTER_CLASS_KEY = 'EXCHANGE_ADAPTER_CLASS'
EXCHANGE_DEFAULT_ADAPTER_CLASS = 'exchange.adapters.xe_exchangerates.XeExchangeRatesAdapter'


def update_rates(adapter_class_name=None):
    update_rates_from_date(adapter_class_name, datetime.date.today())


def update_rates_from_date(adapter_class_name=None, date=None):
    adapter_class_name = (adapter_class_name or
                          getattr(settings, EXCHANGE_ADAPTER_CLASS_KEY, EXCHANGE_DEFAULT_ADAPTER_CLASS))

    adapter_class = import_class(adapter_class_name)
    adapter = adapter_class()
    if not isinstance(adapter, BaseAdapter):
        raise TypeError("invalid adapter class: %s" % adapter_class_name)

    if isinstance(date, basestring):
        from_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        from_date = date if isinstance(date, datetime.date) else datetime.date.today()

    today = datetime.date.today()
    numdays = (today - from_date).days + 1
    date_list = [today - datetime.timedelta(days=x) for x in range(0, numdays)]
    for day in date_list:
        adapter.update_by_day(day)

    if CACHE_ENABLED:
        update_rates_cached()


def convert_values(args_list):
    value_map = {}
    rate_map = {}
    conversions = set([args[1:3] for args in args_list])

    if CACHE_ENABLED:
        rate_map = get_rates_cached(conversions)

    for args in args_list:
        conversion = args[1:3]
        rate = rate_map.get(conversion)
        if not rate:
            rate = ExchangeRate.objects.get_rate(conversion[1], conversion[2])
        value_map[args] = rate

    return value_map


def get_rate(date, source_currency, target_currency):
    rate = None
    if CACHE_ENABLED:
        rate = get_rate_cached(date, source_currency, target_currency)

    if not rate:
        rate = ExchangeRate.objects.get_rate_by_day(source_currency, target_currency, date)

    return rate


def convert_value_by_day(value, source_currency, target_currency, date):
    """Converts the price of a currency to another one using Historical exhange rates

    :param value: the price value
    :param type: decimal

    :param source_currency: source ISO-4217 currency code
    :param type: str

    :param target_currency: target ISO-4217 currency code
    :param type: str

    :param date: historical exchange rate date
    :param type: date

    :returns: converted price instance
    :rtype: ``Money``

    """
    # If price currency and target currency is same
    # return given currency as is
    if source_currency == target_currency:
        return value

    rate = get_rate(date, source_currency, target_currency)
    # value is type Decimal then must first convert rate to Decimal before we can '*' the values
    if isinstance(value, D):
        rate = D(str(rate))

    return value * rate


def convert_price_by_avg_days(price, target_currency, date_from, date_to):
    """Converts the price of a currency to another one using Historical average exhange rates

    :param price: the price value
    :param type: Money

    :param target_currency: target ISO-4217 currency code
    :param type: str

    :param date_from: historical exchange rate date
    :param type: date

    :param date_to: historical exchange rate date
    :param type: date

    :returns: converted price instance
    :rtype: ``Money``
    """

    return convert_value_by_avg_days(price.amount, price.currency, target_currency, date_from, date_to)


def convert_value_by_avg_days(value, source_currency, target_currency, date_from, date_to):
    """Converts the price of a currency to another one using Historical average exhange rates

    :param value: the price value
    :param type: decimal

    :param source_currency: source ISO-4217 currency code
    :param type: str

    :param target_currency: target ISO-4217 currency code
    :param type: str

    :param date_from: historical exchange rate date
    :param type: date

    :param date_to: historical exchange rate date
    :param type: date

    :returns: converted price instance
    :rtype: ``Money``

    """
    # If price currency and target currency is same
    # return given currency as is
    if source_currency == target_currency:
        return value

    rate = ExchangeRate.objects.get_rate_by_avg_days(source_currency, target_currency, date_from, date_to)
    # value is type Decimal then must first convert rate to Decimal before we can '*' the values
    if isinstance(value, D):
        rate = D(str(rate))
    return Money(value * rate, target_currency)


def convert_value(value, source_currency, target_currency):
    """Converts the price of a currency to another one using exhange rates

    :param price: the price value
    :param type: decimal

    :param source_currency: source ISO-4217 currency code
    :param type: str

    :param target_currency: target ISO-4217 currency code
    :param type: str

    :returns: converted price instance
    :rtype: ``Money``

    """
    # If price currency and target currency is same
    # return given currency as is
    return convert_value_by_day(value, source_currency, target_currency, datetime.date.today())


def convert(price, currency):
    """Shorthand function converts a price object instance of a source
    currency to target currency

    :param price: the price value
    :param type: decimal

    :param currency: target ISO-4217 currency code
    :param type: str

    :returns: converted price instance
    :rtype: ``Money``

    """
    # If price currency and target currency is same
    # return given currency as is
    value = convert_value(price.amount, price.currency, currency)
    return Money(value, currency)
