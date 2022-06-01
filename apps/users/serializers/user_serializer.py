from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from phonenumber_field.serializerfields import PhoneNumberField

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.users.models import User, DailyActivity, UserHealthReport, Profile
from apps.users.serializers.profile_serializer import ProfileSerializer

from lib.choices import GENDER


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

    def create(self, validated_data):
        instance = super().create(validated_data)
        profile, _ = Profile.objects.create(user=instance)
        return instance
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile, _ = Profile.objects.get_or_create(user=instance)
            serializer = ProfileSerializer(instance=profile, data=profile_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        user = super().update(instance, validated_data)
        return user


class UserHealthReportSerializer(DynamicFieldsModelSerializer):

    def validate_hemoglobin(self, hemoglobin):
        if not 1 < int(hemoglobin) < 30:
            raise serializers.ValidationError("Enter a value between 1 and 30")
        return hemoglobin
    
    def validate(self, attrs):
        user = self.context.get('user')
        pcod_pcos = attrs.get('pcod_pcos', None)
        if (pcod_pcos is None) and (user.profile.gender == GENDER.female):
            raise serializers.ValidationError("You must provide `pcod_pcos` field for female user")
        elif pcod_pcos and (user.profile.gender == GENDER.male):
            attrs.pop('pcod_pcos')
        
        return attrs
        
    class Meta:
        model = UserHealthReport
        fields = (
            "user", "date", "vitamin_b12", "vitamin_d", "hemoglobin", "uric_acid",
            "creatin", "fasting_blood_sugar", "cholesterol", "thyroid_tsh", "pcod_pcos",
            "dry_skin", "image", "extra_info"
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