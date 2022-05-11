from django.urls import path

# local
from .views import Index, passthought, FirebaseLoginView

app_name = "firebase"

urlpatterns = [
    path("login/", FirebaseLoginView.as_view(), name="firebase-logn"),
    path("<page>", passthought, name="passthought"),
    path("", Index.as_view(), name="index"),
]
