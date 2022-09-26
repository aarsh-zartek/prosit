from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views.generic import TemplateView

from .settings import FIREBASE_CONFIG

CONTEXT = {
    "FIREBASE_CONFIG": FIREBASE_CONFIG['FIREBASE_WEBAPP_CONFIG']
}

class Index(TemplateView):
    template_name = "firebase/auth/index.html"
    extra_context = CONTEXT


def passthough(request, page):
    try:
        context = CONTEXT
        return render(request, f"firebase/auth/{page}", context=context)
    except TemplateDoesNotExist as e:
        return render(request, f"firebase/auth/404.html", context=context)
