from typing import Union
from rest_framework import serializers

from apps.users.models import Profile
from apps.core.serializers import DynamicFieldsModelSerializer


class ProfileSerializer(DynamicFieldsModelSerializer):
    subscription_expires_on = serializers.SerializerMethodField()

    def get_subscription_expires_on(self, instance: Profile) -> Union[str, None]:
        if sub := instance.user.active_subscription:
            return sub.expires_on
        return None
    
    class Meta:
        model = Profile
        fields = (
            "weight", "height", "age",
            "blood_group", "gender", "food_preference",
            "address", "location", "subscription_expires_on",
        )

    def to_representation(self, instance: Profile):
        representation = super().to_representation(instance)
        representation['blood_group'] = instance.get_blood_group_display()
        representation['gender'] = instance.get_gender_display()
        representation['food_preference'] = instance.get_food_preference_display()
        
        return representation
