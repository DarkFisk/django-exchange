from __future__ import absolute_import

import logging
import datetime
import bs4
from django.core.mail import mail_admins
from exchange.models import Currency, ExchangeRate

from django.conf import settings

from exchange.adapters import BaseAdapter
import requests


default_base_curr = ('EUR', 'USD', 'CZK', 'PLN', 'RUB')  # , 'UAH'


class XeExchangeRatesAdapter(BaseAdapter):
    """This adapter uses xe.com service to populate currency and exchange rate models.
    """
    EXCHANGE_BASE_CURRENCIES = 'EXCHANGE_BASE_CURRENCIES'
    url = 'http://www.xe.com/currencytables/?from=%s&date=%s'

    def __init__(self):
        self.base_curr = getattr(settings, self.EXCHANGE_BASE_CURRENCIES, default_base_curr)
        self.client = requests.Session()

    def get_currencies(self):
        final_url = self.url % ('EUR', '2014-10-19')
        response = self.client.get(final_url)
        soup = bs4.BeautifulSoup(response.content)
        curr_links = soup.find('table', attrs={'id': 'historicalRateTbl'}).find('tbody').find_all('a')
        return [(curr_link.text.strip(), curr_link.find_next('td').text.strip()) for curr_link in curr_links]

    def get_exchangerates(self, code):
        return self.get_exchangerates_by_day(code, datetime.date.today())

    def get_exchangerates_by_day(self, code, date):
        final_url = self.url % (code, date.strftime("%Y-%m-%d"))
        response = self.client.get(final_url)
        return self.get_parsed_rate(response)

    def get_parsed_rate(self, response):
        rates = {}
        soup = bs4.BeautifulSoup(response.content)

        error = soup.find('span', attrs={'id': 'ictErrors'})
        if error and error.text.strip():
            return rates

        curr_links = soup.find('table', attrs={'id': 'historicalRateTbl'}).find('tbody').find_all('a')
        for curr_link in curr_links:
            code_name = curr_link.text.strip()
            if code_name in self.base_curr:
                rate = curr_link.find_next('td').find_next('td').text.strip()
                rates[code_name] = rate
        return rates

    def update(self):
        self.update_by_day(datetime.date.today())

    def update_by_day(self, date):
        """Actual update process goes here using auxialary ``get_currencies``
        and ``get_exchangerates`` methods. This method creates or updates
        corresponding ``Currency`` and ``ExchangeRate`` models
        """
        print 'UPDATE EXCHANGE RATE for day: %s' % date
        currencies = self.get_currencies()
        for code, name in currencies:
            if code in self.base_curr:
                _, created = Currency.objects.get_or_create(
                    code=code, defaults={'name': name})
                if created:
                    print('currency: %s created', code)

        for source in Currency.objects.filter(code__in=self.base_curr).all():
            exchange_rates = self.get_exchangerates_by_day(source.code, date)
            if exchange_rates:
                exchange_rates.pop(source.code)
                for code, rate in exchange_rates.iteritems():
                    try:
                        target = Currency.objects.get(code=code)
                        exchange_rate = ExchangeRate.objects.get(date=date, source=source, target=target)
                        exchange_rate.rate = rate
                        exchange_rate.save()
                        print('exchange rate updated %s, %s/%s=%s' % (date, source, target, rate))
                    except ExchangeRate.DoesNotExist:
                        exchange_rate = ExchangeRate.objects.create(date=date, source=source, target=target, rate=rate)
                        print('exchange rate created %s, %s/%s=%s' % (date, source, target, rate))
            else:
                print('There is no rate for the current day')
                mail_admins('Exchange Rates Warning', 'There is no today exchange rate')
                break
