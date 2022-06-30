from rest_framework.permissions import BasePermission

from apps.users.models import User, user

from lib.constants import Subscription

class IsSubscribed(BasePermission):
	message = "No active subscription found"

	def has_permission(self, request, view):
		user = request.user
		return user.subscriptions.filter(
				subscription_status=Subscription.SubscriptionStatus.ACTIVE
			).exists()


class HasActivePlan(BasePermission):
	message = "Your plan is being generated"
	
	def has_permission(self, request, view):

		return request.user.subscriptions.filter(
				subscription_status=Subscription.SubscriptionStatus.ACTIVE,
				plan__isnull=False
			).exists()