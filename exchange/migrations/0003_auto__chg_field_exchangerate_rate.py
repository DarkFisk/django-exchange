# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ExchangeRate.rate'
        db.alter_column(u'exchange_exchangerate', 'rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=5))

    def backwards(self, orm):

        # Changing field 'ExchangeRate.rate'
        db.alter_column(u'exchange_exchangerate', 'rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2))

    models = {
        u'exchange.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'exchange.exchangerate': {
            'Meta': {'unique_together': "(('date', 'source', 'target'),)", 'object_name': 'ExchangeRate'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '5'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rates'", 'null': 'True', 'to': u"orm['exchange.Currency']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']", 'null': 'True'})
        }
    }

    complete_apps = ['exchange']