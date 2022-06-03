from django.contrib import admin

# Register your models here.

from apps.plan.models import DietPlan, PlanCategory


class PlanCategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "no_of_plans", "created")

	def no_of_plans(self, instance):
		return instance.diet_plans.count()

class DietPlanAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "plan_type", "parent", "created")
	list_filter = ("plan_type",)


admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(PlanCategory, PlanCategoryAdmin)