# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ExchangeRate.date'
        db.add_column(u'exchange_exchangerate', 'date',
                      self.gf('django.db.models.fields.DateField')(null=True, db_index=True),
                      keep_default=False)


        # Changing field 'ExchangeRate.source'
        db.alter_column(u'exchange_exchangerate', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['exchange.Currency']))

        # Changing field 'ExchangeRate.rate'
        db.alter_column(u'exchange_exchangerate', 'rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2))

        # Changing field 'ExchangeRate.target'
        db.alter_column(u'exchange_exchangerate', 'target_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'], null=True))
        # Adding unique constraint on 'ExchangeRate', fields ['date', 'source', 'target']
        db.create_unique(u'exchange_exchangerate', ['date', 'source_id', 'target_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ExchangeRate', fields ['date', 'source', 'target']
        db.delete_unique(u'exchange_exchangerate', ['date', 'source_id', 'target_id'])

        # Deleting field 'ExchangeRate.date'
        db.delete_column(u'exchange_exchangerate', 'date')


        # Changing field 'ExchangeRate.source'
        db.alter_column(u'exchange_exchangerate', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['exchange.Currency']))

        # Changing field 'ExchangeRate.rate'
        db.alter_column(u'exchange_exchangerate', 'rate', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=12, decimal_places=2))

        # Changing field 'ExchangeRate.target'
        db.alter_column(u'exchange_exchangerate', 'target_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['exchange.Currency']))

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
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rates'", 'null': 'True', 'to': u"orm['exchange.Currency']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']", 'null': 'True'})
        }
    }

    complete_apps = ['exchange']