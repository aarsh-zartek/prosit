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
        "health_report_uploaded",
        "health_code",
    )
    readonly_fields = ("expires_on", "health_code")
    list_filter = ("subscription_status",)
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    def get_readonly_fields(self, request, obj):
        read_only_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            read_only_fields += (
                "amount_paid",
                "receipt",
            )

        return read_only_fields


admin.site.register(UserSubscription, UserSubscriptionAdmin)
