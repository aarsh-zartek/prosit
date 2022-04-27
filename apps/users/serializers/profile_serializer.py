from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import Profile
from apps.core.serializers import DynamicFieldsModelSerializer


class ProfileSerializer(DynamicFieldsModelSerializer):

	token = serializers.SerializerMethodField()
	
	def get_token(self, instance):
		return Token.objects.get_or_create(instance)
	
	class Meta:
		model = Profile
		fields = ("token",)
		# extra_fields = [
		# 	"token",
		# ]