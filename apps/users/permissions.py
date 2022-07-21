from rest_framework.permissions import BasePermission

class IsSubscribed(BasePermission):
	message = "No active subscription found"

	def has_permission(self, request, view):
		return True if request.user.active_subscription else False


class HasActivePlan(BasePermission):
	message = "Your plan is being generated"
	
	def has_permission(self, request, view):
		return True if request.user.active_plan else False
