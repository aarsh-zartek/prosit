from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# Register your models here.

from apps.plan.models import DietPlan, PlanCategory, QuestionAnswer


class PlanCategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "no_of_plans", "created")

	def no_of_plans(self, instance):
		return instance.diet_plans.count()


class QuestionAnswerAdmin(admin.ModelAdmin):
	list_display = ("diet_plan", "question", "answer")


class QuestionAnswerInline(admin.TabularInline):
	model = QuestionAnswer


class DietPlanAdmin(admin.ModelAdmin):
	list_display = ("name", "get_category", "plan_type", "parent", "no_of_questions", "created")
	list_filter = ("plan_type",)
	inlines = (QuestionAnswerInline,)

	def no_of_questions(self, instance):
		return instance.question_answers.count()
	
	def get_category(self, instance: DietPlan):
		link = (
			reverse("admin:plan_plancategory_changelist")  + "?" + urlencode({"id": instance.category.id})
		)
		return format_html('<b><a href="{}">{}</a></b>', link, instance.category)
	get_category.short_description = "Plan Category"


admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(PlanCategory, PlanCategoryAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)