from django.utils.translation import gettext_lazy as _

from model_utils import Choices

from lib.constants import (
    CancellationReason,
    Device,
    Environment,
    EventType,
    PeriodType,
    Store,
    SubscriptionPeriod,
    SubscriptionStatus,
)

PLAN_TYPES = Choices(
    (_("main_category"), ("Main Category")),
    (_("sub_category"), ("Sub Category")),
)

FIELDS_TO_SHOW = Choices(
    (_("vitamin_b12"), _("Vitamin B12")),
    (_("vitamin_d"), _("Vitamin D")),
    (_("uric_acid"), _("Uric Acid")),
    (_("creatin"), _("Creatin")),
    (_("fasting_blood_sugar"), _("Fasting Blood Sugar")),
    (_("cholesterol"), _("Cholesterol")),
    (_("hemoglobin"), _("Hemoglobin")),
    (_("thyroid_tsh"), _("Thyroid (TSH)")),
    (_("dry_skin"), _("Dry Skin")),
    (_("pcod_pcos"), _("PCOD / PCOS")),
)

GENDER = Choices(
    (_("male"), _("Male")),
    (_("female"), _("Female")),
    (_("other"), _("Other")),
)

FOOD_PREFERENCES = Choices(
    (_("vegetarian"), _("Vegetarian")),
    (_("non_vegetarian"), _("Non Vegetarian")),
)

BLOOD_GROUP_CHOICES = Choices(
    (_("a+"), _("a_positive"), _("A +ve")),
    (_("b+"), _("b_positive"), _("B +ve")),
    (_("o+"), _("o_positive"), _("O +ve")),
    (_("ab+"), _("ab_positive"), _("AB +ve")),
    (_("a-"), _("a_negative"), _("A -ve")),
    (_("b-"), _("b_negative"), _("B -ve")),
    (_("o-"), _("o_negative"), _("O -ve")),
    (_("ab-"), _("ab_negative"), _("AB -ve")),
)

DEVICE_CHOICES = Choices(
    (Device.ANDROID, _("Android")),
    (Device.IOS, _("iOS")),
    (Device.WEB, _("Web"))
)

SUBSCRIPTION_PERIOD_CHOICES = (
    (SubscriptionPeriod.MONTHLY, _("monthly")),
    (SubscriptionPeriod.YEARLY, _("yearly")),
)

EVENT_TYPE_CHOICES = Choices(
    (EventType.TEST, _("Test")),
    (EventType.INITIAL_PURCHASE, _("Initial Purchase")),
    (EventType.NON_RENEWING_PURCHASE, _("Non Renewing Purchase")),
    (EventType.RENEWAL, _("Renewal")),
    (EventType.PRODUCT_CHANGE, _("Product Change")),
    (EventType.CANCELLED, _("Cancelled")),
    (EventType.BILLING_ISSUE, _("Billing Issue")),
    (EventType.SUBSCRIBER_ALIAS, _("Subscriber Alias")),
)

ENVIRONMENT_CHOICES = Choices(
    (Environment.SANDBOX, _("Sandbox")),
    (Environment.PRODUCTION, _("Production")),
)


STORE_CHOICES = Choices(
    (Store.PLAY_STORE, _("Play Store")),
    (Store.APP_STORE, _("App Store")),
    (Store.STRIPE, _("Stripe")),
    (Store.MAC_APP_STORE, _("Mac App Store")),
    (Store.PROMOTIONAL, _("Promotional")),
)


PERIOD_TYPE_CHOICES = Choices(
    (PeriodType.TRIAL, _("Trial")),
    (PeriodType.INTRO, _("Intro")),
    (PeriodType.NORMAL, _("Normal")),
    (PeriodType.PROMOTIONAL, _("Promotional")),
)

CANCELLATION_REASON_CHOICES = Choices(
    (CancellationReason.UNSUBSCRIBE, _("Unsubscribe")),
    (CancellationReason.BILLING_ERROR, _("Billing Error")),
    (CancellationReason.DEVELOPER_INITIATED, _("Developer Initiated")),
    (CancellationReason.PRICE_INCREASE, _("Price Increase")),
    (CancellationReason.CUSTOMER_SUPPORT, _("Customer Support")),
    (CancellationReason.UNKNOWN, _("Unknown")),
)

SUBSCRIPTION_STATUS_CHOICES = Choices(
    (SubscriptionStatus.ACTIVE, _("Active")),
    (SubscriptionStatus.EXPIRED, _("Expired")),
    (SubscriptionStatus.CANCELLED, _("Cancelled")),
)
