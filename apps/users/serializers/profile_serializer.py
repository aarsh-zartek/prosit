from rest_framework import serializers

from apps.users.models import Profile
from apps.core.serializers import DynamicFieldsModelSerializer


class ProfileSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            "weight", "height", "age",
            "blood_group", "gender", "food_preference",
            "address", "location",
        )

    def to_representation(self, instance: Profile):
        representation = super().to_representation(instance)
        representation['blood_group'] = instance.get_blood_group_display()
        representation['gender'] = instance.get_gender_display()
        representation['food_preference'] = instance.get_food_preference_display()
        
        return representation