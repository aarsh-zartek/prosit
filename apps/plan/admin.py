from django.contrib import admin

# Register your models here.

from apps.plan.models import DietPlan, UserDietPlan, PlanType


class PlanTypeAdmin(admin.ModelAdmin):
	list_display = ("name", "created")


class DietPlanAdmin(admin.ModelAdmin):
	list_display = ("name", "plan_type")


admin.site.register(PlanType, PlanTypeAdmin)
admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(UserDietPlan)