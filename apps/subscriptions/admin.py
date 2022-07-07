from django.contrib import admin

from apps.subscriptions.models import Subscription


# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ("user", "plan", "amount_paid", "payment_status", "subscription_status", "expires_on")
	readonly_fields=('expires_on', "transaction_id")
	list_filter = ("subscription_status", "payment_status")


admin.site.register(Subscription, SubscriptionAdmin)