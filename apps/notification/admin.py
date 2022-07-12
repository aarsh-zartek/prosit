from django.contrib import admin

from apps.notification.models import UserNotification

# Register your models here.


class UserNotificationAdmin(admin.ModelAdmin):

    list_display = ( "user", "title", "message", "read_at",)
    list_filter = ("read_at",)
    

admin.site.register(UserNotification, UserNotificationAdmin)