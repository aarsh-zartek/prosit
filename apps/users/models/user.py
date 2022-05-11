from django.db import models
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook

from apps.core.models import BaseModel
from apps.firebase.models import AbstractFirebaseUser

from lib.constants import FieldConstants
from lib.utils import get_user_health_image_path

# Create your models here.

class User(LifecycleModelMixin, BaseModel, AbstractFirebaseUser):
    """Default `Prosit` User which inherits from AbstractFirebaseUser"""

    first_name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH, null=True)
    last_name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH, null=True)
    
    # category = models.ForeignKey(PlanCategory, on_delete=models.SET_NULL, blank=True, null=True)

    @hook(AFTER_CREATE)
    def after_create(self):
        category = self.assign_category()    
        # self.category = category

    class Meta:
        ordering = ("created",)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else (self.display_name if self.display_name else "")
    
    @property
    def full_name(self) -> str:
        return self.__str__()

    def assign_category(self):
        return "new_category"    

    def delete(self):
        self.is_active = False
        self.save()


class MedicalCondition(BaseModel):
    medical_condition = models.CharField(verbose_name=_("Medical Conditions"), max_length=FieldConstants.MAX_NAME_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_conditions")

    class Meta:
        verbose_name = _("Medical Condition")
        verbose_name_plural = _("Medical Conditions")


class FoodAllergy(BaseModel):
    food_allergy = models.CharField(verbose_name=_("Food Allergies"), max_length=FieldConstants.MAX_NAME_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_allergies")

    class Meta:
        verbose_name = _("Food Allergy")
        verbose_name_plural = _("Food Allergies")


class UserHealthReport(BaseModel):
    """Model which stores data for lab tests for a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    date = models.DateField()
    
    blood_sugar_level = models.CharField(max_length=48, blank=True, null=True)
    blood_pressure_level = models.CharField(max_length=48, blank=True, null=True)
    cholestrol_count = models.CharField(max_length=48, blank=True, null=True)
    thyroid_count = models.CharField(max_length=48, blank=True, null=True)
    image = models.ImageField(upload_to=get_user_health_image_path, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('User Health Report')
        verbose_name_plural = _('User Health Reports')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name=_("user_health_report_date_unique")
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.date}'


class DailyActivity(BaseModel):
    """
    Model to track the daily activity of users such as weight
    """
    
    user = models.ForeignKey(User, related_name="daily_activity", on_delete=models.CASCADE)

    weight = models.PositiveSmallIntegerField(verbose_name=_("Weight in KG"))
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name=_("user_date_unique")
            )
        ]