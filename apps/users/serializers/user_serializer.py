from datetime import datetime

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from dateutil import parser

from phonenumber_field.serializerfields import PhoneNumberField

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.users.models import User, DailyActivity
from apps.users.serializers.profile_serializer import ProfileSerializer


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, instance):
        token, created = Token.objects.get_or_create(user=instance)
        return token.key
    
    class Meta:
        model = User
        fields = ["token", "uid", "display_name"]


class UserSerializer(DynamicFieldsModelSerializer):
    """User model serializer for users."""

    password = serializers.CharField(required=False, write_only=True)
    phone_number = PhoneNumberField(required=False)
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = (
            "id", "uid", "display_name", "password", "phone_number",
            "email", "first_name", "last_name", "profile",
        )


class DailyActivitySerializer(serializers.ModelSerializer):
    """To track daily user activity

    `weight` is a non-editable field
    
    `date` must be less than or equal to today's date
    """

    def validate_date(self, date_value):
        today = datetime.today().date()
        if date_value > today:
            raise serializers.ValidationError("Date must be less than today")
        return date_value
    
    class Meta:
        model = DailyActivity
        fields = ("user", "weight", "date")
