from django.contrib import admin

# Register your models here.

from apps.plan.models import DietPlan, UserDietPlan

admin.site.register(DietPlan)
admin.site.register(UserDietPlan)