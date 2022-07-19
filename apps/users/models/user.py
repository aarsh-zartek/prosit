from django.db import models
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook

from apps.core.models import BaseModel
from apps.firebase.models import AbstractFirebaseUser
# from apps.notification.tasks import send_email_notificaton
from apps.users.utils import get_category

from lib.constants import FieldConstants, SubscriptionStatus
from lib.utils import get_user_health_image_path, get_profile_picture_path

# Create your models here.

class User(LifecycleModelMixin, BaseModel, AbstractFirebaseUser):
    """Default `Prosit` User which inherits from AbstractFirebaseUser"""

    first_name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    last_name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    profile_picture = models.ImageField(upload_to=get_profile_picture_path, blank=True, null=True)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("created",)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self) -> str:
        return self.__str__()

    def delete(self):
        self.is_active = False
        self.save()

    @property
    def active_subscription(self):
        if user_subscription := self.subscriptions.filter(subscription_status=SubscriptionStatus.ACTIVE):
            return user_subscription.latest("created")
        return None
    
    @property
    def active_plan(self):
        return self.active_subscription.plan if self.active_subscription else None


class UserHealthReport(LifecycleModelMixin, BaseModel):
    """Model which stores data for lab tests of a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    date = models.DateField(verbose_name=_("Reports Generated On"), auto_now_add=True)
    
    vitamin_b12 = models.BooleanField(verbose_name=_("Vitamin B12"))
    vitamin_d = models.BooleanField(verbose_name=_("Vitamin D"))
    uric_acid = models.BooleanField(verbose_name=_("Uric Acid"))
    creatin = models.BooleanField(verbose_name=_("Creatin"))
    fasting_blood_sugar = models.PositiveSmallIntegerField(verbose_name=_("Fasting Blood Sugar"))
    cholesterol = models.PositiveSmallIntegerField(verbose_name=_("Cholesterol"))
    hemoglobin = models.PositiveSmallIntegerField(verbose_name=_("Hemoglobin"))
    thyroid_tsh = models.BooleanField(verbose_name=_("Thyroid (TSH)"))
    dry_skin = models.BooleanField(verbose_name=_("Dry Skin"), default=False)
    pcod_pcos = models.BooleanField(
                verbose_name=_("PCOD / PCOS"),
                blank=True, default=False
            )
    
    health_code = models.CharField(verbose_name=_("User Health Code"), max_length=FieldConstants.MAX_HEALTH_CODE_LENGTH, null=True, editable=False)
    
    image = models.ImageField(upload_to=get_user_health_image_path, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('User Health Report')
        verbose_name_plural = _('User Health Reports')
        unique_together = ("user", "date")

    def __str__(self) -> str:
        return f'{self.user} - {self.date}'

    @hook(hook=AFTER_CREATE)
    def after_create(self):
        if not self.health_code:
            health_code = self._assign_health_code()
            if health_code_users := User.objects.filter(health_reports__health_code=health_code):
                # add plan to current user subscription
                pass
                # self.user.active_subscription.plan = health_code_users.first().
            else:
                # notify_admin?
                pass
                # send_email_notificaton(message="", admins=True)

    def _assign_health_code(self) -> str:
        profile = self.user.profile
        
        weight = round(profile.weight)
        gender = profile.get_gender_display()[0]
        food_preference = profile.get_food_preference_display()[0]
        category = self._assign_category()

        health_code = f"{weight:03}{gender}{food_preference}{category}"
        self.health_code = health_code
        # self.user.profile.health_code = health_code

        return health_code

    def _assign_category(self) -> str:
        category_data = {
            "vitamin_b12": self.vitamin_b12,
            "vitamin_d": self.vitamin_d,
            "uric_acid": self.uric_acid,
            "creatin": self.creatin,
            "fasting_blood_sugar": self.fasting_blood_sugar,
            "hemoglobin": self.hemoglobin,
            "thyroid_tsh": self.thyroid_tsh,
            "pcod_pcos": self.pcod_pcos,
            "gender": self.user.profile.gender,
        }

        return get_category(category_data)

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError

        if not self.user.active_subscription:
            raise ValidationError("No Active subscription found")
        
        return super().save(*args, **kwargs)


class DailyActivity(BaseModel):
    """
    Model to track the daily activity of users such as weight
    """
    
    user = models.ForeignKey(User, related_name="daily_activity", on_delete=models.CASCADE)

    weight = models.DecimalField(
                verbose_name=_("Weight in KG"),
                max_digits=5, decimal_places=2
            )
    date = models.DateTimeField()

    class Meta:
        verbose_name = _("Daily Activity")
        verbose_name_plural = _("Daily Activities")
        unique_together = ('user', 'date')
    
    def __str__(self) -> str:
        return f"{self.user} - {self.date} - {self.weight}"
