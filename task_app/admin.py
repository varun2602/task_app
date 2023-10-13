from django.contrib import admin
from . import models 
from django.contrib.sessions.models import Session

admin.site.register(models.Task)

admin.site.register(models.Users)

admin.site.register(models.otp_verification)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "expire_date", "get_decoded_session_data")
    def get_decoded_session_data(self, obj):
        return obj.get_decoded
    get_decoded_session_data.short_description = "Session Data"