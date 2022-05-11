from django.contrib import admin

# Register your models here.

from apps.plan.models import DietPlan, PlanCategory


class PlanCategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "created")


class DietPlanAdmin(admin.ModelAdmin):
	list_display = ("name", "plan_category")


admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(PlanCategory, PlanCategoryAdmin)