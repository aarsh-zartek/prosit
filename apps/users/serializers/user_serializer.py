from rest_framework import serializers
from rest_framework.authtoken.models import Token

# from djoser.conf import settings

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.users.models.user import User

class TokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, instance):
        token, created = Token.objects.get_or_create(user=instance)

        return token.key
    
    class Meta:
        model = User
        fields = ["token", "uid", "display_name"]


class UserSerializer(DynamicFieldsModelSerializer):
        
    class Meta:
        model = User
        fields = "__all__"


# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)