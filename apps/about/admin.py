from django.contrib import admin

from apps.about.models import Company, FAQ

# Register your models here.

class FAQAdmin(admin.ModelAdmin):
	list_display = ("company", "question", "answer")


class FAQInline(admin.TabularInline):
	model = FAQ


class CompanyAdmin(admin.ModelAdmin):
	list_display = ("home_page_title", "home_page_text", "contact_number")
	inlines = (FAQInline,)


admin.site.register(Company, CompanyAdmin)
admin.site.register(FAQ, FAQAdmin)