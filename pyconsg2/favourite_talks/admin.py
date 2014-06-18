"""Admin classes for the favourite_talks app."""
from django.contrib import admin

from . import models


class UserPresentationAdmin(admin.ModelAdmin):
    model = models.UserPresentation
    list_display = [
        'id', 'user__email', 'presentation__title',
    ]
    list_filter = ['presentation', ]
    raw_id_fields = ['user', ]

    def user__email(self, obj):
        return obj.user.email

    def presentation__title(self, obj):
        return obj.presentation.title


admin.site.register(models.UserPresentation, UserPresentationAdmin)
