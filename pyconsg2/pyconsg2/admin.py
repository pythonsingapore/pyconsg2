"""Admin overrides for the pyconsg2 project."""
from django.contrib import admin

from account.models import EmailAddress


class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'verified', 'primary', )
    list_filter = ('verified', 'primary', )
    search_fields = ('user__username', 'email', )


admin.site.register(EmailAddress, EmailAddressAdmin)
