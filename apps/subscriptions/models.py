from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.plan.models import DietPlan
from apps.users.models import User

from lib.choices import PAYMENT_METHODS, PAYMENT_STATUSES, SUBSCRIPTION_STATUSES
from lib.constants import FieldConstants

# Create your models here.


class Subscription(BaseModel):

	user = models.ForeignKey(
			to=User,
			on_delete=models.CASCADE,
			related_name="subscriptions"
		)
	plan = models.ForeignKey(
			to=DietPlan,
			on_delete=models.PROTECT,
			related_name="subscribers",
			blank=True,
			null=True
		)

	amount_paid = models.PositiveIntegerField(verbose_name=_("Amount Paid"))
	transaction_id = models.CharField(
		verbose_name=_("Transaction ID"),
		max_length=FieldConstants.MAX_LENGTH,
		editable=False
	)

	payment_method = models.CharField(
		verbose_name=_("Payment Method"),
		max_length=FieldConstants.MAX_NAME_LENGTH,
		choices=PAYMENT_METHODS
	)
	payment_status = models.CharField(
		verbose_name=_("Payment Status"),
		max_length=FieldConstants.MAX_NAME_LENGTH,
		choices=PAYMENT_STATUSES
	)
	subscription_status = models.CharField(
		verbose_name=_("Subscription Status"),
		max_length=FieldConstants.MAX_NAME_LENGTH,
		choices=SUBSCRIPTION_STATUSES
	)
	
	expires_on = models.DateTimeField(
		verbose_name=_("Subscription Expires On"),
		null=True, editable=False,
	)

	class Meta:
		verbose_name = _("Subscription")
		verbose_name_plural = _("User Subscriptions")

	def __str__(self) -> str:
		return f'{self.user.full_name} - {self.plan.name} - {self.get_subscription_status_display()}'

