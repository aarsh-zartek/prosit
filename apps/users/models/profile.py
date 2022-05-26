from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User

from lib.choices import BLOOD_GROUP_CHOICES, GENDER, FOOD_PREFERENCES
from lib.constants import FieldConstants

# Create your models here.


class Profile(BaseModel):
    """
    Model which holds additional user information
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    weight = models.DecimalField(
                verbose_name=_("Weight in KG"),
                blank=True, null=True,
                max_digits=5, decimal_places=2
            )
    height = models.DecimalField(
                verbose_name=_("Height in CM"),
                blank=True, null=True,
                max_digits=5, decimal_places=2
            )
    age = models.PositiveSmallIntegerField(verbose_name=_("Age in Years"), null=True)
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, blank=True, null=True, max_length=8)
    gender = models.CharField(choices=GENDER, max_length=8, default=_(GENDER.male))
    food_preference = models.CharField(choices=FOOD_PREFERENCES, max_length=20, default=_(FOOD_PREFERENCES.vegetarian))
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=FieldConstants.MAX_LENGTH, blank=True, null=True)

    class Meta:
        verbose_name = _("User Profile")

    def __str__(self) -> str:
        return f"{self.user} - {self.gender} - {self.age}"

