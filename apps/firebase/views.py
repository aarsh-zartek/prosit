from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .settings import FIREBASE_CONFIG

from firebase_admin.auth import create_custom_token

from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from apps.users.models import User
from apps.users.serializers.user_serializer import UserSerializer

class Index(TemplateView):
    template_name = "firebase/auth/index.html"
    extra_context = {
        "FIREBASE_CONFIG": FIREBASE_CONFIG['FIREBASE_WEBAPP_CONFIG'],
    }


def passthought(request, page):
    context = {
        "FIREBASE_CONFIG": FIREBASE_CONFIG['FIREBASE_WEBAPP_CONFIG'],
    }
    return render(request, f"firebase/auth/{page}", context=context)


class FirebaseLoginView(APIView):
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_number=request.data.get('phone_number'))
        except User.DoesNotExist:
            return JsonResponse(data={
                "message": "User does not exist"
            }, status=HTTP_401_UNAUTHORIZED)
        else:
            token = create_custom_token(uid=user.uid).decode('utf8')
            return JsonResponse(data={
                    "firebase_access_token": token
                }, status=HTTP_200_OK
            )