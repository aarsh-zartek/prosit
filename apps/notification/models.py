from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User

from lib.constants import FieldConstants

# Create your models here.


class Notification(BaseModel):

	user = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="notifications",
	)
	title = models.CharField(
		verbose_name=_("Title"),
		max_length=FieldConstants.MAX_LENGTH
	)
	message = models.CharField(
		verbose_name=_("Message"),
		max_length=FieldConstants.MAX_LENGTH
	)

	read_at = models.DateTimeField(blank=True, null=True)


	class Meta:
		verbose_name = _('Notification')
		verbose_name_plural = _('User Notifications')
		ordering = ('-created',)
	
	def __str__(self) -> str:
		return f"{self.title}"
