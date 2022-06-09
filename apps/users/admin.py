from django.contrib import admin
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import TokenProxy
from apps.users.models import User, Profile, UserHealthReport, DailyActivity
# Register your models here.

admin.site.site_header = "Prosit Admin Panel"
admin.site.site_title = "Prosit Site Administration"
admin.site.index_title = "Admin Panel"
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "weight", "height", "gender", "health_code")
    readonly_fields=('health_code',)

    def full_name(self, instance):
        return instance.user.full_name


class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'uid', 'phone_number', 'email', 'is_active')
    list_filter = ("is_active", "is_staff")
    search_fields = ("phone_number", "uid", "first_name", "last_name", "display_name")
    inlines = [ProfileInline,]


class UserHealthReportAdmin(admin.ModelAdmin):
    list_display = (
        "user", "date", "vitamin_b12", "vitamin_d",
        "creatin", "fasting_blood_sugar",
        "hemoglobin", "thyroid_tsh", "dry_skin",
    )

class DailyActvityAdmin(admin.ModelAdmin):
    list_display = ("user", "weight", "date")
    list_filter = ("date",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserHealthReport, UserHealthReportAdmin)
admin.site.register(DailyActivity, DailyActvityAdmin)
