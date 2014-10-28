import datetime
from decimal import Decimal
from django.db import models
from django.db.models import Avg


class ExchangeRateManager(models.Manager):
    def get_query_set(self):
        return super(ExchangeRateManager, self).get_query_set().select_related('source', 'target')

    def get_rate(self, source_currency, target_currency):
        return self.get_rate_by_day(source_currency, target_currency, datetime.date.today())

    def get_rate_by_day(self, source_currency, target_currency, date):
        return self.get(source__code=source_currency,
                        target__code=target_currency,
                        date=date).rate

    def get_rate_by_avg_days(self, source_currency, target_currency, date_from, date_to):
        return self.filter(source__code=source_currency,
                           target__code=target_currency,
                           date__range=(date_from, date_to)).aggregate(Avg('rate')).values()[0] or Decimal()
