# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TopMacro.created_at'
        db.add_column(u'stats_topmacro', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'ShootingStar.created_at'
        db.add_column(u'stats_shootingstar', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SinkingStone.created_at'
        db.add_column(u'stats_sinkingstone', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TopMacro.created_at'
        db.delete_column(u'stats_topmacro', 'created_at')

        # Deleting field 'ShootingStar.created_at'
        db.delete_column(u'stats_shootingstar', 'created_at')

        # Deleting field 'SinkingStone.created_at'
        db.delete_column(u'stats_sinkingstone', 'created_at')


    models = {
        u'stats.imagemacro': {
            'Meta': {'object_name': 'ImageMacro'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        u'stats.meme': {
            'Meta': {'object_name': 'Meme'},
            'classification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classification'", 'null': 'True', 'to': u"orm['stats.ImageMacro']"}),
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fullSizeLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_corrupt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'threadLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'topCorr': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'topDist': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'stats.potentialimagemacro': {
            'Meta': {'object_name': 'PotentialImageMacro'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fullSizeLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'threadLink': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailLink': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'stats.shootingstar': {
            'Meta': {'object_name': 'ShootingStar'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        },
        u'stats.sinkingstone': {
            'Meta': {'object_name': 'SinkingStone'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        },
        u'stats.topmacro': {
            'Meta': {'object_name': 'TopMacro'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['stats']