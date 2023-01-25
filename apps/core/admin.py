from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

# Register your models here.

class GroupAdmin(BaseGroupAdmin):
    list_display = (
        "name", "permission_count", "user_count"
    )

    def permission_count(self, instance: Group):
        return instance.permissions.count()
    
    def user_count(self, instance: Group):
        return instance.user_set.count()
    
    permission_count.short_description = "Permission Count"
    user_count.short_description = "User Count"

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
