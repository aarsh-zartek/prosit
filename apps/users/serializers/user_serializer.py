from datetime import datetime

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator

from phonenumber_field.serializerfields import PhoneNumberField

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.users.models import User, DailyActivity, UserHealthReport
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
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "id", "uid", "display_name", "password", "phone_number",
            "email", "first_name", "last_name", "profile",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)
        if profile_data:
            serializer = ProfileSerializer(instance=user.profile, data=profile_data)
            serializer.is_valid()
            serializer.save()
        return user


class UserHealthReportSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = UserHealthReport
        fields = (
            "date", "vitamin_b12", "vitamin_d", "hemoglobin", "uric_acid",
            "creatin", "fasting_blood_sugar", "thyroid_tsh", "pcod_pcos",
            "image"
        )
    

class DailyActivitySerializer(serializers.ModelSerializer):
    """To track daily user activity

    `weight` is a non-editable field
    
    `date` must be less than or equal to today's date
    """

    def validate_date(self, date_value):
        today = datetime.today().date()
        if date_value > today:
            raise serializers.ValidationError("Date must be less than or equal to today's date")
        return date_value
    
    class Meta:
        model = DailyActivity
        fields = ("user", "weight", "date")
        validators = [
            UniqueTogetherValidator(
                queryset=DailyActivity.objects.all(),
                fields=["user", "date"]
            )
        ]