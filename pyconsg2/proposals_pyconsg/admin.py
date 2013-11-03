from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from symposion.schedule.models import Presentation

from . import models


class PresentationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'speaker', 'speaker_user_email', 'slot', 'proposal_kind',
    ]

    list_filter = ['proposal_base__kind__name', ]

    def proposal_kind(self, obj):
        return obj.proposal_base.kind

    def speaker_user_email(self, obj):
        return obj.speaker.user.email


class TalkProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'speaker_email', 'submitted']

    def speaker_email(self, obj):
        u = User.objects.get(email=obj.speaker.email)
        url = reverse("admin:%s_%s_change" % (
            u._meta.app_label, u._meta.module_name), args=(u.pk,))
        return '<a href="%s">%s<a/>' % (url, obj.speaker.email)
    speaker_email.allow_tags = True


class TutorialProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'speaker_email', 'submitted']

    def speaker_email(self, obj):
        u = User.objects.get(email=obj.speaker.email)
        url = reverse("admin:%s_%s_change" % (
            u._meta.app_label, u._meta.module_name), args=(u.pk,))
        return '<a href="%s">%s<a/>' % (url, obj.speaker.email)
    speaker_email.allow_tags = True


admin.site.register(models.TalkProposal, TalkProposalAdmin)
admin.site.register(models.TutorialProposal, TutorialProposalAdmin)

admin.site.unregister(Presentation)
admin.site.register(Presentation, PresentationAdmin)
