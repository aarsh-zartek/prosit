from django.utils.translation import gettext_lazy as _

from model_utils import Choices

from lib.constants import DietPlanCategory, Subscription


PLAN_CATEGORIES = Choices(
    (DietPlanCategory.MALYALAM_DIET, _("Malyalam Diet")),
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


PAYMENT_METHODS = Choices(
    (_("wallet"), Subscription.PaymentMethod.WALLET),
    (_("credit_card"), Subscription.PaymentMethod.CREDIT_CARD),
    (_("debit_card"), Subscription.PaymentMethod.DEBIT_CARD),
    (_("upi"), Subscription.PaymentMethod.UPI),
    (_("wallet"), Subscription.PaymentMethod.WALLET),
)

PAYMENT_STATUSES = Choices(
    (_("pending"), Subscription.PaymentStatus.PENDING),
    (_("processing"), Subscription.PaymentStatus.PROCESSING),
    (_("successful"), Subscription.PaymentStatus.SUCCESSFUL),
    (_("failed"), Subscription.PaymentStatus.FAILED),
    (_("rejected"), Subscription.PaymentStatus.REJECTED),
)

SUBSCRIPTION_STATUSES = Choices(
    (_("inactive"), Subscription.SubscriptionStatus.INACTIVE),
    (_("active"), Subscription.SubscriptionStatus.ACTIVE),
    (_("expired"), Subscription.SubscriptionStatus.EXPIRED),

)