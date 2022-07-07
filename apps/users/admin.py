from typing import Any, Optional

from django.http import HttpRequest
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

    def get_queryset(self, request: HttpRequest):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.exclude(user__is_superuser=True)

        return queryset


class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'uid', 'phone_number', 'email', 'is_active')
    list_filter = ("is_active", "is_staff")
    search_fields = ("phone_number", "uid", "first_name", "last_name", "display_name")
    inlines = [ProfileInline,]

    def get_form(self, request: Any, obj: Optional[User]=..., change: bool=..., **kwargs: Any):

        if not request.user.is_superuser:
            self.exclude = ("is_superuser",)
        
        return super().get_form(request, obj, change, **kwargs)

    def get_queryset(self, request: HttpRequest):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)

        return queryset

    def get_readonly_fields(self, request: HttpRequest, obj: Optional[User]):
        read_only_fields = super().get_readonly_fields(request, obj)

        if not request.user.is_superuser:
            read_only_fields += ("is_staff",)
        
        return read_only_fields


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
