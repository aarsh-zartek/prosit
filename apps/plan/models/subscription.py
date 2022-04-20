from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User


# class UserSubscription(BaseModel):

# 	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')	
    
# 	class Meta:
# 		verbose_name = _('User Subscriptions')