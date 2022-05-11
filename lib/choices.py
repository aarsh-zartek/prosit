from django.utils.translation import gettext_lazy as _

from model_utils import Choices

from lib.constants import DietPlanCategory, DietPlanType


PLAN_CATEGORIES = Choices(
    (DietPlanCategory.MALYALAM_DIET, _("Malyalam Diet")),
)

PLAN_TYPES = Choices(
    (DietPlanType.WEIGHT_LOSS_PLAN, _("Weight Loss Plan")),
    (DietPlanType.WEIGHT_GAIN_PLAN, _("Weight Gain Plan")),
    (DietPlanType.GYM_FITNESS_PLAN, _("Gym Fitness Plan")),
    (DietPlanType.BALANCED_DIET_PLAN, _("Balanced Diet Plan")),
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
