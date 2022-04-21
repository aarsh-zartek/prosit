from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User

from lib.constants import FieldConstants, AudioFormats, DocumentFormats
from lib.utils import get_diet_plan_instruction_path

# Create your models here


class PlanType(BaseModel):
    name = models.CharField(verbose_name=_("Plan Type"), max_length=FieldConstants.MAX_NAME_LENGTH)
    instruction_text = models.TextField(blank=True, null=True, help_text=_("Instructions for the user in text format"))
    instruction_audio = models.FileField(
                            verbose_name="Instruction in Audio",
                            upload_to=get_diet_plan_instruction_path,
                            validators=[
                                FileExtensionValidator(allowed_extensions=AudioFormats.all())
                            ],
                            blank=True,
                            null=True
                        )
    instruction_pdf = models.FileField(
                        verbose_name="Instruction in Pdf",
                        upload_to=get_diet_plan_instruction_path,
                        validators=[
                            FileExtensionValidator(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )

    class Meta:
        verbose_name = _("Plan Type")
        verbose_name_plural = _("Plan Types")
    
    def __str__(self) -> str:
        return f"{self.name}"


class DietPlan(BaseModel):
    name = models.CharField(verbose_name=_("Diet Plan Name"), max_length=FieldConstants.MAX_NAME_LENGTH)
    plan_type = models.ForeignKey(PlanType, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("Diet Plan")
        verbose_name_plural = _("Diet Plans")
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'plan_type'],
                name=_("diet_plan_category")
            )
        ]


    def __str__(self) -> str:
        return f"{self.name} - {self.plan_type.name}"


class UserDietPlan(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_plan')
    plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='user_plan')
    date_started = models.DateField()
    valid_until = models.DateField()

    class Meta:
        verbose_name = _("User Diet Plan")
        verbose_name_plural = _("User Diet Plans")
