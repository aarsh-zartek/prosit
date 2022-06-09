from django.urls import include, path

from apps.about.views import CompanyView

urlpatterns = [
	path("about", view=CompanyView.as_view(), name="about")
]