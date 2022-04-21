from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.firebase.models import AbstractFirebaseUser

from lib.choices import GENDER_TYPES, FOOD_PREFERENCES
from lib.utils import get_user_health_image_path

# Create your models here.

class User(BaseModel, AbstractFirebaseUser):
    """Default user for prosit which inherits from FirebaseUser"""
    pass

    def delete(self):
        self.is_active = False
        self.save()



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name=_("Age in Years"), blank=True, null=True)
    blood_group = models.CharField(blank=True, null=True, max_length=8)
    gender = models.CharField(choices=GENDER_TYPES, max_length=8)
    food_preference = models.CharField(choices=FOOD_PREFERENCES, max_length=20)
    
  

class UserHealthReport(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    date = models.DateField()
    
    blood_sugar_level = models.CharField(max_length=48, blank=True, null=True)
    blood_pressure_level = models.CharField(max_length=48, blank=True, null=True)
    cholestrol_count = models.CharField(max_length=48, blank=True, null=True)
    thyroid_count = models.CharField(max_length=48, blank=True, null=True)
    image = models.ImageField(upload_to=get_user_health_image_path, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.date}'