from django.contrib import admin

from apps.subscriptions.models import UserSubscription


# Register your models here.

class UserSubscriptionAdmin(admin.ModelAdmin):
	list_display = ("user", "plan", "amount_paid", "subscription_status", "expires_on")
	readonly_fields=('expires_on', "receipt")
	list_filter = ("subscription_status",)


admin.site.register(UserSubscription, UserSubscriptionAdmin)
