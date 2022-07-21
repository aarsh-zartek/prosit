from django.contrib import admin

from apps.about.models import Company, ContactForm, FAQ

# Register your models here.

class FAQAdmin(admin.ModelAdmin):
	list_display = ("company", "question", "answer")


class FAQInline(admin.TabularInline):
	model = FAQ


class CompanyAdmin(admin.ModelAdmin):
	list_display = ("home_page_title", "home_page_text", "contact_number")
	inlines = (FAQInline,)

class ContactFormAdmin(admin.ModelAdmin):
	list_display = ("user", "name", "email", "phone_number", "created")
	list_filter = ("created",)
	search_fields = ("user__first_name", "user__last_name", "phone_number")


admin.site.register(Company, CompanyAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ContactForm, ContactFormAdmin)
