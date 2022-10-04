from django.db import models
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook

from apps.core.models import BaseModel
from apps.firebase.models import AbstractFirebaseUser
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

    def delete(self, hard=False):
        """Deletes a user object

        Args:
            hard (bool, optional): To hard delete User. Defaults to False.
        """
        if hard:
            super().delete()
        else:
            self.is_active = False
            self.save()

    @property
    def active_subscription(self):
        """
        Returns the Latest, Active User Subscription or `None`
        """
        if user_subscription := self.subscriptions.filter(subscription_status=SubscriptionStatus.ACTIVE):
            return user_subscription.latest("created")
        return None
    
    @property
    def active_plan(self):
        """
        Returns the active User Plan or `None`
        """
        return self.active_subscription.plan if self.active_subscription else None


class UserHealthReport(LifecycleModelMixin, BaseModel):
    """Model which stores data for lab tests of a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    date = models.DateField(verbose_name=_("Reports Generated On"), auto_now_add=True)
    
    vitamin_b12 = models.BooleanField(verbose_name=_("Vitamin B12"))
    vitamin_d = models.BooleanField(verbose_name=_("Vitamin D"))
    uric_acid = models.BooleanField(verbose_name=_("Uric Acid"))
    creatin = models.BooleanField(verbose_name=_("Creatin"))
    fasting_blood_sugar = models.DecimalField(
        verbose_name=_("Fasting Blood Sugar"),
        max_digits=5, decimal_places=2
    )
    cholesterol = models.DecimalField(
        verbose_name=_("Cholesterol"),
        max_digits=5, decimal_places=2
    )
    hemoglobin = models.DecimalField(
        verbose_name=_("Hemoglobin"),
        max_digits=5, decimal_places=2
    )
    thyroid_tsh = models.BooleanField(verbose_name=_("Thyroid (TSH)"))
    dry_skin = models.BooleanField(verbose_name=_("Dry Skin"), default=False)
    pcod_pcos = models.BooleanField(
                verbose_name=_("PCOD / PCOS"),
                blank=True, default=False
            )
    
    health_code = models.CharField(
        verbose_name=_("User Health Code"),
        max_length=FieldConstants.MAX_HEALTH_CODE_LENGTH,
        null=True,
        editable=False
    )
    
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
        health_code = self._assign_health_code()
        subscription = self.user.active_subscription
        subscription.health_report = self
        subscription.save()
        reports = self.get_similar_health_reports()
        
        if reports:
            # add plan to current user subscription
            #? TODO
            # subscription.plan = reports.last().user.subscriptions.last().plan
            subscription.plan = reports.last().subscription.plan
            subscription.save()
        else:
            # notify_admin
            from apps.notification.tasks import send_email_notificaton
            data = {
                "id": self.user.id,
                "name": self.user.display_name or self.user.full_name,
                "phone_number": self.user.phone_number.as_international,
                "health_code": health_code
            }
            send_email_notificaton.apply_async(args=(data,), kwargs={"admin": True})

    def _assign_health_code(self) -> str:
        """Assigns a health code to user based on profile """
        profile = self.user.profile
        
        weight = round(profile.weight)
        gender = profile.get_gender_display()[0]
        food_preference = profile.get_food_preference_display()[0]
        category = self._assign_category()

        health_code = f"{weight:03}{gender}{food_preference}{category}"
        self.health_code = health_code
        self.save()

        return health_code

    def _assign_category(self) -> str:
        """
        Returns a category from `A` to `L` or `0` based on
        his profile & health reports
        """

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

    def get_similar_health_reports(self):
        reports = UserHealthReport.objects.select_related("user").prefetch_related(
            "subscription"
        ).exclude(
            id=self.id
        ).filter(
            health_code=self.health_code,
            subscription__receipt__plan_id=self.subscription.receipt["plan_id"]
        )
        return reports

    def clean(self) -> None:
        from django.core.exceptions import ValidationError

        if not self.user.active_subscription:
            raise ValidationError("No Active Subscription found for this user")

        return super().clean()


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
