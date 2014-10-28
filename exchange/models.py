from django.db import models
from exchange.managers import ExchangeRateManager
from exchange.iso_4217 import code_list


class Currency(models.Model):
    """Model holds a currency information for a nationality"""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return self.code

    def get_numeric_code(self):
        return code_list[self.code]  # Let it raise an exception


class ExchangeRate(models.Model):
    """Model to persist exchange rates between currencies"""
    date = models.DateField(null=True, db_index=True)
    source = models.ForeignKey(Currency, null=True, related_name='rates')
    target = models.ForeignKey(Currency, null=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    objects = ExchangeRateManager()

    class Meta:
        unique_together = ('date', 'source', 'target')

    def __unicode__(self):
        return '%s, %s / %s = %s' % (self.date, self.source, self.target, self.rate)
