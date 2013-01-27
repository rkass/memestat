# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageMacro'
        db.create_table('stats_imagemacro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('stats', ['ImageMacro'])

        # Adding model 'Meme'
        db.create_table('stats_meme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classification', null=True, to=orm['stats.ImageMacro'])),
            ('thumbnailLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('fullSizeLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('submitter', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('topCorr', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('topDist', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.IntegerField')()),
            ('threadLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('img_corrupt', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stats', ['Meme'])

        # Adding model 'PotentialImageMacro'
        db.create_table('stats_potentialimagemacro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('thumbnailLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('fullSizeLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('submitter', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.IntegerField')()),
            ('threadLink', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('stats', ['PotentialImageMacro'])


    def backwards(self, orm):
        # Deleting model 'ImageMacro'
        db.delete_table('stats_imagemacro')

        # Deleting model 'Meme'
        db.delete_table('stats_meme')

        # Deleting model 'PotentialImageMacro'
        db.delete_table('stats_potentialimagemacro')


    models = {
        'stats.imagemacro': {
            'Meta': {'object_name': 'ImageMacro'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'stats.meme': {
            'Meta': {'object_name': 'Meme'},
            'classification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classification'", 'null': 'True', 'to': "orm['stats.ImageMacro']"}),
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fullSizeLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_corrupt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'threadLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'topCorr': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'topDist': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'stats.potentialimagemacro': {
            'Meta': {'object_name': 'PotentialImageMacro'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fullSizeLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'threadLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailLink': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['stats']