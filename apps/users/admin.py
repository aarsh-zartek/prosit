from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

from apps.users.models import User, UserHealthReport, Profile

admin.site.site_header = "Prosit Admin Panel"
admin.site.site_title = "Prosit Site Administration"
admin.site.index_title = "Admin Panel Administration"
admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'display_name', 'email', 'is_active')


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(UserHealthReport)