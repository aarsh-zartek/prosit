from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User

from lib.choices import BLOOD_GROUP_CHOICES, GENDER, FOOD_PREFERENCES

# Create your models here.


class Profile(BaseModel):
    """
    Model which holds additional user information
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name=_("Age in Years"), null=True)
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, blank=True, null=True, max_length=8)
    gender = models.CharField(choices=GENDER, max_length=8, default=_(GENDER.male))
    food_preference = models.CharField(choices=FOOD_PREFERENCES, max_length=20, default=_(FOOD_PREFERENCES.vegetarian))

    class Meta:
        verbose_name = _("User Profile")

    def __str__(self) -> str:
        return f"{self.user} - {self.gender} - {self.age}"

