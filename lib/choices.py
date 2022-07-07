from django.utils.translation import gettext_lazy as _

from model_utils import Choices

from lib.constants import SubscriptionConstants


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


PAYMENT_METHODS = Choices(
    (SubscriptionConstants.PaymentMethod.WALLET, _("Wallet")),
    (SubscriptionConstants.PaymentMethod.CREDIT_CARD, _("Credit Card")),
    (SubscriptionConstants.PaymentMethod.DEBIT_CARD, _("Debit Card")),
    (SubscriptionConstants.PaymentMethod.UPI, _("UPI")),
    (SubscriptionConstants.PaymentMethod.WALLET, _("Wallet")),
)

PAYMENT_STATUSES = Choices(
    (SubscriptionConstants.PaymentStatus.PENDING, _("Pending")),
    (SubscriptionConstants.PaymentStatus.PROCESSING, _("Processing")),
    (SubscriptionConstants.PaymentStatus.SUCCESSFUL, _("Successful")),
    (SubscriptionConstants.PaymentStatus.FAILED, _("Failed")),
    (SubscriptionConstants.PaymentStatus.REJECTED, _("Rejected")),
)

SUBSCRIPTION_STATUSES = Choices(
    (SubscriptionConstants.SubscriptionStatus.INACTIVE, _("Inactive")),
    (SubscriptionConstants.SubscriptionStatus.ACTIVE, _("Active")),
    (SubscriptionConstants.SubscriptionStatus.EXPIRED, _("Expired")),

)