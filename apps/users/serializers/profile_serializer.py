from rest_framework import serializers

from apps.users.models import Profile
from apps.core.serializers import DynamicFieldsModelSerializer


class ProfileSerializer(DynamicFieldsModelSerializer):
    blood_group = serializers.CharField(source="get_blood_group_display", required=False)
    gender = serializers.CharField(source="get_gender_display", required=False)
    food_preference = serializers.CharField(source="get_food_preference_display", required=False)
    
    class Meta:
        model = Profile
        fields = (
            "weight", "height", "age",
            "blood_group", "gender", "food_preference",
            "address", "location",
        )
