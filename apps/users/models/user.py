from django.core.validators import validate_integer
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
        verbose_name = _("User")
        verbose_name_plural = _("Users")
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

class UserHealthReport(BaseModel):
    """Model which stores data for lab tests of a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    date = models.DateField(verbose_name=_("Reports Generated On"))
    
    vitamin_b12 = models.BooleanField(verbose_name=_("Vitamin B12"))
    vitamin_d = models.BooleanField(verbose_name=_("Vitamin D"))
    uric_acid = models.BooleanField(verbose_name=_("Uric Acid"))
    creatin = models.BooleanField(verbose_name=_("Creatin"))
    fasting_blood_sugar = models.CharField(
                verbose_name=_("Fasting Blood Sugar"),
                max_length=FieldConstants.MAX_VALUE_LENGTH,
            )
    cholestrol = models.CharField(
                verbose_name=_("Cholestrol"),
                max_length=FieldConstants.MAX_VALUE_LENGTH,
                validators=[validate_integer,],
            )
    hemoglobin = models.CharField(
                verbose_name=_("Hemoglobin"),
                max_length=FieldConstants.MAX_VALUE_LENGTH,
            )
    thyroid_tsh = models.BooleanField(verbose_name=_("Thyroid TSH"))
    pcod_pcos = models.BooleanField(
                verbose_name=_("PCOD / PCOS"),
                blank=True, default=False
            )
    
    image = models.ImageField(upload_to=get_user_health_image_path, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('User Health Report')
        verbose_name_plural = _('User Health Reports')
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user', 'date'],
        #         name=_("user_health_report_date_unique")
        #     )
        # ]
        unique_together = ("user", "date")

    def __str__(self) -> str:
        return f'{self.user} - {self.date}'


class DailyActivity(BaseModel):
    """
    Model to track the daily activity of users such as weight
    """
    
    user = models.ForeignKey(User, related_name="daily_activity", on_delete=models.CASCADE)

    weight = models.DecimalField(
                verbose_name=_("Weight in KG"),
                max_digits=5, decimal_places=2
            )
    date = models.DateField()

    class Meta:
        verbose_name = _("Daily Activity")
        verbose_name_plural = _("Daily Activities")
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name=_("user_date_unique")
            )
        ]
    
    def __str__(self) -> str:
        return f"{self.user} - {self.date} - {self.weight}"
