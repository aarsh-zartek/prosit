from django.urls import path

from apps.about.views import CompanyView, ContactFormView, FAQView

urlpatterns = [
	path("about", view=CompanyView.as_view(), name="about-company"),
	path("contact/", view=ContactFormView.as_view(), name="contact-form"),
	path("faq", view=FAQView.as_view(), name="faq"),
]
