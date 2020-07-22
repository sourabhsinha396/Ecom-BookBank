from django.contrib import admin

from .models import MarkettingPreference

class MarkettingPreferenceAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'subscribed', ]
    # readonly_fields = ['mailchimp_msg', 'mailchimp_subscribed', 'timestamp', ]
    class Meta:
        model = MarkettingPreference
        fields = [
                    'user',
                    'subscribed',
                    'mailchimp_subscribed',
                    'mailchimp_msg',
                ]

admin.site.register(MarkettingPreference, MarkettingPreferenceAdmin)
