from django.urls import path

# local
from .views import Index, passthought

app_name = "firebase"

urlpatterns = [
    path("<page>", passthought, name="passthought"),
    path("", Index.as_view(), name="index"),
]
