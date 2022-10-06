from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.subscriptions.models import UserSubscription


# Register your models here.


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "amount_paid",
        "subscription_status",
        "expires_on",
        "get_health_report_uploaded",
    )
    readonly_fields = ("expires_on",)
    list_filter = ("subscription_status",)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    # form = UserSubscriptionForm

    def get_readonly_fields(self, request, obj):
        read_only_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            read_only_fields += ("receipt",)

        return read_only_fields
    
    @admin.display(boolean=True, description="Health Reports Uploaded?")
    def get_health_report_uploaded(self, instance: UserSubscription):
        return instance.health_report_uploaded


admin.site.register(UserSubscription, UserSubscriptionAdmin)
