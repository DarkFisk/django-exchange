# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'exchange_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('exchange', ['Currency'])

        # Adding model 'ExchangeRate'
        db.create_table(u'exchange_exchangerate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rates', to=orm['exchange.Currency'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'])),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('exchange', ['ExchangeRate'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'exchange_currency')

        # Deleting model 'ExchangeRate'
        db.delete_table(u'exchange_exchangerate')


    models = {
        'exchange.currency': {
            'Meta': {'unique_together': '()', 'object_name': 'Currency', 'index_together': '()'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'exchange.exchangerate': {
            'Meta': {'object_name': 'ExchangeRate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rates'", 'to': "orm['exchange.Currency']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exchange.Currency']"})
        }
    }

    complete_apps = ['exchange']