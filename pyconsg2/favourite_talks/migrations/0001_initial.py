# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserPresentation'
        db.create_table(u'favourite_talks_userpresentation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('presentation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Presentation'])),
        ))
        db.send_create_signal(u'favourite_talks', ['UserPresentation'])


    def backwards(self, orm):
        # Deleting model 'UserPresentation'
        db.delete_table(u'favourite_talks_userpresentation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'UTC'", 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'conference.section': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Section'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.Conference']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'favourite_talks.userpresentation': {
            'Meta': {'object_name': 'UserPresentation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Presentation']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'proposals.additionalspeaker': {
            'Meta': {'unique_together': "(('speaker', 'proposalbase'),)", 'object_name': 'AdditionalSpeaker', 'db_table': "'proposals_proposalbase_additional_speakers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposalbase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalBase']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['speakers.Speaker']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'proposals.proposalbase': {
            'Meta': {'object_name': 'ProposalBase'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_additional_notes_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_notes': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['speakers.Speaker']", 'symmetrical': 'False', 'through': u"orm['proposals.AdditionalSpeaker']", 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': u"orm['speakers.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'proposals.proposalkind': {
            'Meta': {'object_name': 'ProposalKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposal_kinds'", 'to': u"orm['conference.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'schedule.day': {
            'Meta': {'ordering': "['date']", 'unique_together': "[('schedule', 'date')]", 'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Schedule']"})
        },
        u'schedule.presentation': {
            'Meta': {'ordering': "['slot']", 'object_name': 'Presentation'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_description_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'copresentations'", 'blank': 'True', 'to': u"orm['speakers.Speaker']"}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal_base': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'presentation'", 'unique': 'True', 'to': u"orm['proposals.ProposalBase']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': u"orm['conference.Section']"}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'content_ptr'", 'unique': 'True', 'null': 'True', 'to': u"orm['schedule.Slot']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': u"orm['speakers.Speaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'schedule.schedule': {
            'Meta': {'ordering': "['section']", 'object_name': 'Schedule'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'section': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conference.Section']", 'unique': 'True'})
        },
        u'schedule.slot': {
            'Meta': {'ordering': "['day', 'start', 'end']", 'object_name': 'Slot'},
            '_content_override_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_override': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.SlotKind']"}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        u'schedule.slotkind': {
            'Meta': {'object_name': 'SlotKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Schedule']"})
        },
        u'speakers.speaker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speaker'},
            '_biography_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['favourite_talks']