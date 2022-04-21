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

GENDER_TYPES = Choices(
    (_("male"), _("Male")),
    (_("female"), _("Female")),
    (_("other"), _("Other")),
)

FOOD_PREFERENCES = Choices(
    (_("vegetarian"), _("Vegetarian")),
    (_("non_vegetarian"), _("Non Vegetarian")),
)