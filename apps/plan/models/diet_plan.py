from django.core.validators import FileExtensionValidator as FEV
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from lib.constants import FieldConstants, AudioFormats, DocumentFormats
from lib.utils import get_diet_plan_instruction_path, get_preparation_path

# Create your models here


class PlanCategory(BaseModel):
    name = models.CharField(verbose_name=_("Category Name"), max_length=FieldConstants.MAX_NAME_LENGTH)
    instruction_text_in_english = models.TextField()
    instruction_text_in_malayalam = models.TextField()

    instruction_audio_in_english = models.FileField(
            verbose_name="Instruction Audio in English",
            upload_to=get_diet_plan_instruction_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )
    instruction_audio_in_malayalam = models.FileField(
            verbose_name="Instruction Audio in Malayalam",
            upload_to=get_diet_plan_instruction_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )

    instruction_pdf_in_english = models.FileField(
                        verbose_name="Instruction in Pdf",
                        upload_to=get_diet_plan_instruction_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )
    instruction_pdf_in_malayalam = models.FileField(
                        verbose_name="Instruction in Pdf",
                        upload_to=get_diet_plan_instruction_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )

    preparation_instruction_text_english = models.TextField()
    preparation_instruction_text_malayalam = models.TextField()

    preparation_instruction_audio_english = models.FileField(
            verbose_name="Preparation Instruction Audio in English",
            upload_to=get_preparation_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )
    preparation_instruction_audio_malayalam = models.FileField(
            verbose_name="Preparation Instruction Audio in Malayalam",
            upload_to=get_preparation_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )

    class Meta:
        verbose_name = _("Plan Category")
        verbose_name_plural = _("Plan Categories")
    
    def __str__(self) -> str:
        return self.name


class DietPlan(BaseModel):
    name = models.CharField(verbose_name=_("Diet Plan Name"), max_length=FieldConstants.MAX_NAME_LENGTH)
    plan_category = models.ForeignKey(PlanCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="diet_plans")
    value = models.PositiveIntegerField(verbose_name=_("Plan Value"))

    class Meta:
        verbose_name = _("Diet Plan")
        verbose_name_plural = _("Diet Plans")
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'plan_category'],
                name=_("diet_plan_category")
            )
        ]


    def __str__(self) -> str:
        return f"{self.name} - {self.plan_category}"
