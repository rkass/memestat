# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopMacro'
        db.create_table(u'stats_topmacro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dailyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('dailyChange', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyChange', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stats', ['TopMacro'])

        # Adding M2M table for field macros on 'TopMacro'
        db.create_table(u'stats_topmacro_macros', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topmacro', models.ForeignKey(orm[u'stats.topmacro'], null=False)),
            ('imagemacro', models.ForeignKey(orm[u'stats.imagemacro'], null=False))
        ))
        db.create_unique(u'stats_topmacro_macros', ['topmacro_id', 'imagemacro_id'])

        # Adding model 'ShootingStar'
        db.create_table(u'stats_shootingstar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dailyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('dailyChange', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyChange', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stats', ['ShootingStar'])

        # Adding M2M table for field macros on 'ShootingStar'
        db.create_table(u'stats_shootingstar_macros', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shootingstar', models.ForeignKey(orm[u'stats.shootingstar'], null=False)),
            ('imagemacro', models.ForeignKey(orm[u'stats.imagemacro'], null=False))
        ))
        db.create_unique(u'stats_shootingstar_macros', ['shootingstar_id', 'imagemacro_id'])

        # Adding model 'SinkingStone'
        db.create_table(u'stats_sinkingstone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dailyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyScore', self.gf('django.db.models.fields.IntegerField')()),
            ('dailyChange', self.gf('django.db.models.fields.IntegerField')()),
            ('hourlyChange', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stats', ['SinkingStone'])

        # Adding M2M table for field macros on 'SinkingStone'
        db.create_table(u'stats_sinkingstone_macros', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sinkingstone', models.ForeignKey(orm[u'stats.sinkingstone'], null=False)),
            ('imagemacro', models.ForeignKey(orm[u'stats.imagemacro'], null=False))
        ))
        db.create_unique(u'stats_sinkingstone_macros', ['sinkingstone_id', 'imagemacro_id'])


    def backwards(self, orm):
        # Deleting model 'TopMacro'
        db.delete_table(u'stats_topmacro')

        # Removing M2M table for field macros on 'TopMacro'
        db.delete_table('stats_topmacro_macros')

        # Deleting model 'ShootingStar'
        db.delete_table(u'stats_shootingstar')

        # Removing M2M table for field macros on 'ShootingStar'
        db.delete_table('stats_shootingstar_macros')

        # Deleting model 'SinkingStone'
        db.delete_table(u'stats_sinkingstone')

        # Removing M2M table for field macros on 'SinkingStone'
        db.delete_table('stats_sinkingstone_macros')


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
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        },
        u'stats.sinkingstone': {
            'Meta': {'object_name': 'SinkingStone'},
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        },
        u'stats.topmacro': {
            'Meta': {'object_name': 'TopMacro'},
            'dailyChange': ('django.db.models.fields.IntegerField', [], {}),
            'dailyScore': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyChange': ('django.db.models.fields.IntegerField', [], {}),
            'hourlyScore': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'macros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stats.ImageMacro']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['stats']