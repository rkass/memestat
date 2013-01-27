# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ImageMacro.name'
        db.add_column('stats_imagemacro', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=1000, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ImageMacro.name'
        db.delete_column('stats_imagemacro', 'name')


    models = {
        'stats.imagemacro': {
            'Meta': {'object_name': 'ImageMacro'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
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