from django.urls import path

from apps.about.views import CompanyView, ContactFormView

urlpatterns = [
	path("about", view=CompanyView.as_view(), name="about-company"),
	path("contact/", view=ContactFormView.as_view(), name="contact-form"),
]
