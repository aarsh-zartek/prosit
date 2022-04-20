from django.contrib import admin

# Register your models here.

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'full_name', 'email', 'is_active')


admin.site.register(User, UserAdmin)