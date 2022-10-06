from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE

from apps.core.models import BaseModel
from apps.plan.models import DietPlan
from apps.subscriptions.services import RevenueCatService
from apps.users.models import User, UserHealthReport

from lib.utils import one_month_from_today

from lib.choices import (
    EVENT_TYPE_CHOICES,
    ENVIRONMENT_CHOICES,
    STORE_CHOICES,
    PERIOD_TYPE_CHOICES,
    CANCELLATION_REASON_CHOICES,
    SUBSCRIPTION_PERIOD_CHOICES,
    SUBSCRIPTION_STATUS_CHOICES,
)

from lib.constants import (
    FieldConstants,
    SubscriptionIdentifier,
    SubscriptionPeriod,
    SubscriptionStatus,
)

# Create your models here.


class UserSubscription(LifecycleModelMixin, BaseModel):
    """Model definition for saving Subscription details locally."""

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        to=DietPlan,
        on_delete=models.PROTECT,
        related_name="subscribers",
        blank=True,
        null=True,
    )
    health_report = models.OneToOneField(
        to=UserHealthReport,
        related_name="subscription",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    receipt = models.JSONField(verbose_name=_("Subscription Receipt"))
    subscription_type = models.CharField(
        verbose_name=_("Subscription Type"),
        max_length=8,
        choices=SUBSCRIPTION_PERIOD_CHOICES,
        default=SubscriptionPeriod.MONTHLY,
    )

    amount_paid = models.PositiveIntegerField(
        verbose_name=_("Amount Paid"), blank=True, null=True
    )

    subscription_status = models.CharField(
        verbose_name=_("Subscription Status"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        default=SUBSCRIPTION_STATUS_CHOICES.active,
    )
    expires_on = models.DateTimeField(
        verbose_name=_("Subscription Expires on"),
        blank=True,
        default=one_month_from_today,
    )

    class Meta:
        """Meta definition for User Subscription."""

        verbose_name = _("User Subscription")
        verbose_name_plural = _("User Subscriptions")

    def __str__(self):
        """Unicode representation of Subscription."""
        name = self.user.full_name
        user_plan = self.plan.name if self.plan else "Not Assigned"
        sub_status = self.get_subscription_status_display()
        return f"{name} - {user_plan} - {sub_status}"
    
    @property
    def health_report_uploaded(self):
        return True if self.health_report else False

    @hook(hook=AFTER_UPDATE, when="plan", has_changed=True, is_not=None)
    def after_update(self):
        health_code = self.health_report.health_code
        subscriptions = UserSubscription.objects.exclude(
            health_report__isnull=True
        ).filter(
            subscription_status=SubscriptionStatus.ACTIVE,
            health_report__health_code=health_code,
            plan__isnull=True,
            receipt__plan_id=self.plan.id
        )
        if subscriptions:
            subscriptions.update(plan=self.plan)

    def clean(self) -> None:
        initial_status: str = self.initial_value("subscription_status")
        if initial_status != SubscriptionStatus.ACTIVE:
            raise ValidationError(
                f"Can't edit {initial_status} subscriptions"
            )
        
        if not self.health_report_uploaded:
            raise ValidationError("No Health Report uploaded for this user.")

        return super().clean()


class RevenueCatHistory(BaseModel):
    """Model definition for saving subscription details from RevenueCat."""

    # Field Definition
    event_type = models.CharField(
        verbose_name=_("Event Type"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=EVENT_TYPE_CHOICES,
        help_text="Visit https://docs.revenuecat.com/docs/webhooks#section-event-types",
    )

    event_id = models.UUIDField(
        verbose_name=_("Event ID"),
        help_text="Unique identifier of the event for revenue cat",
    )

    event_timestamp = models.DateTimeField(
        verbose_name=_("Event Timestamp"),
        help_text="The time that the event was generated. "
        "Does not necessarily coincide with when the action "
        "that triggered the event occurred (purchased, cancelled, etc).",
    )

    app_user_id = models.CharField(
        verbose_name=_("App User ID"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        help_text="Last seen app user id of the subscriber.",
    )

    original_app_user_id = models.CharField(
        verbose_name=_("Original User ID"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        help_text="The first app user id used by the subscriber.",
    )

    # Aliases

    product_id = models.CharField(
        verbose_name=_("Product ID"),
        max_length=FieldConstants.MAX_LENGTH,
        help_text="Product Identifier of the subscription",
    )

    # Entitlement IDs

    period_type = models.CharField(
        verbose_name=_("Period Type"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=PERIOD_TYPE_CHOICES,
        help_text="Period type of the transaction. "
        "TRIAL, for free trials. "
        "INTRO, for introductory pricing. "
        "NORMAL, standard subscription. "
        "PROMOTIONAL, for subscriptions granted through RevenueCat.",
    )

    purchased_at = models.DateTimeField(verbose_name=_("Purchased at"))

    expiration_at = models.DateTimeField(
        verbose_name=_("Expiration at"),
        null=True,
        help_text="Expiration of the transaction. "
        "Measured in milliseconds since Unix epoch. "
        "Use this field to determine if a subscription is still active."
        "It can be NULL for non-subscription purchases",
    )

    store = models.CharField(
        verbose_name=_("Store"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=STORE_CHOICES,
        help_text="Store the subscription belongs to.",
    )

    environment = models.CharField(
        verbose_name=_("Environment"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=ENVIRONMENT_CHOICES,
    )

    cancellation_reason = models.CharField(
        verbose_name=_("Cancellation Reason"),
        max_length=FieldConstants.MAX_NAME_LENGTH,
        choices=CANCELLATION_REASON_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for RevenueCatHistory."""

        verbose_name = "RevenueCat History"
        verbose_name_plural = "RevenueCat Histories"

    def __str__(self):
        """Unicode representation of RevenueCatHistory."""
        return f"{self.app_user_id}"  # TODO

    @property
    def purchased_at_ms(self):
        return self.purchased_at.timestamp()

    @purchased_at_ms.setter
    def purchased_at_ms(self, value):
        value /= 1000.0
        self.purchased_at = datetime.utcfromtimestamp(value)

    @property
    def expiration_at_ms(self):
        return self.expiration_at.timestamp()

    @expiration_at_ms.setter
    def expiration_at_ms(self, value):
        value /= 1000.0
        self.expiration_at = datetime.utcfromtimestamp(value)

    @property
    def event_timestamp_ms(self):
        return self.event_timestamp.timestamp()

    @event_timestamp_ms.setter
    def event_timestamp_ms(self, value):
        value /= 1000.0
        self.event_timestamp = datetime.utcfromtimestamp(value)

    def is_cancelled(self):
        rc = RevenueCatService(self.app_user_id)
        response = rc.get_response()
        if response.status_code != 200:
            return False

        json = response.json()
        subscriptions = json["subscriber"]["subscriptions"]
        for sub in subscriptions:
            unsubscribe_detected_at = subscriptions[sub]["unsubscribe_detected_at"]
            if unsubscribe_detected_at is None:
                return False
        return True

    @classmethod
    def has_purchased_product(cls, app_user_id):
        rc = RevenueCatService(app_user_id)
        response = rc.get_response()

        if response.status_code != 200:
            return False

        json = response.json()
        non_subscriptions = json["subscriber"]["non_subscriptions"]
        for product, purchases in non_subscriptions.items():
            if product == SubscriptionIdentifier.ONE_MONTH_PLAN:
                for purchase in purchases:
                    original_purchase_date = datetime.strptime(
                        purchase["original_purchase_date"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if (
                        original_purchase_date + timezone.timedelta(days=356)
                        > timezone.now()
                    ):
                        return True
        return False
