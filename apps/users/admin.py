from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

from apps.users.models import User, Profile, UserHealthReport, FoodAllergy, MedicalCondition, DailyActivity

admin.site.site_header = "Prosit Admin Panel"
admin.site.site_title = "Prosit Site Administration"
admin.site.index_title = "Admin Panel"
admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'uid', 'phone_number', 'email', 'is_active')
    list_filter = ("is_active", "is_staff")
    search_fields = ("phone_number", "email", "full_name")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "weight", "height", "gender")

    def full_name(self, instance):
        return instance.user.full_name


class DailyActvityAdmin(admin.ModelAdmin):
    list_display = ("user", "weight", "date")
    list_filter = ("date",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserHealthReport)
admin.site.register(FoodAllergy)
admin.site.register(MedicalCondition)
admin.site.register(DailyActivity, DailyActvityAdmin)