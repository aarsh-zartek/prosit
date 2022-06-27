from datetime import timedelta

from django.core.validators import FileExtensionValidator as FEV
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField

from apps.core.models import BaseModel
from apps.users.models import User

from lib.constants import FieldConstants, AudioFormats, DocumentFormats
from lib.choices import PLAN_TYPES, FIELDS_TO_SHOW, PAYMENT_METHODS, PAYMENT_STATUSES, SUBSCRIPTION_STATUSES
from lib.utils import get_diet_plan_instruction_path, get_preparation_path

# Create your models here


class PlanCategory(BaseModel):
    name = models.CharField(verbose_name=_("Category Name"), max_length=FieldConstants.MAX_NAME_LENGTH)

    per_day_instructions_english = RichTextField(
            verbose_name=_("Per Day Instructions English"), 
            blank=True, null=True
        )
    per_day_instructions_malayalam = RichTextField(
            verbose_name=_("Per Day Instructions Malayalam"), 
            blank=True, null=True
        )

    instruction_text_english = models.TextField()
    instruction_text_malayalam = models.TextField()

    instruction_audio_english = models.FileField(
            verbose_name="Instruction Audio in English",
            upload_to=get_diet_plan_instruction_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )
    instruction_audio_malayalam = models.FileField(
            verbose_name="Instruction Audio in Malayalam",
            upload_to=get_diet_plan_instruction_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )

    instruction_pdf_english = models.FileField(
                        verbose_name=_("Instruction PDF in English"),
                        upload_to=get_diet_plan_instruction_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )
    instruction_pdf_malayalam = models.FileField(
                        verbose_name=_("Instruction PDF in Malayalam"),
                        upload_to=get_diet_plan_instruction_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )

    preparation_text_english = models.TextField()
    preparation_text_malayalam = models.TextField()

    preparation_audio_english = models.FileField(
            verbose_name="Preparation Instruction Audio in English",
            upload_to=get_preparation_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )
    preparation_audio_malayalam = models.FileField(
            verbose_name="Preparation Instruction Audio in Malayalam",
            upload_to=get_preparation_path,
            validators=[
                FEV(allowed_extensions=AudioFormats.all())
            ],
            blank=True,
            null=True
    )

    preparation_pdf_english = models.FileField(
                        verbose_name=_("Preparation PDF in English"),
                        upload_to=get_preparation_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )
    preparation_pdf_malayalam = models.FileField(
                        verbose_name=_("Preparation PDF in Malayalam"),
                        upload_to=get_preparation_path,
                        validators=[
                            FEV(allowed_extensions=DocumentFormats.all())
                        ],
                        blank=True,
                        null=True
                    )

    fields_required = MultiSelectField(choices=FIELDS_TO_SHOW, min_choices=3)
    
    class Meta:
        verbose_name = _("Plan Category")
        verbose_name_plural = _("Plan Categories")
    
    def __str__(self) -> str:
        return self.name


class DietPlan(BaseModel):
    name = models.CharField(verbose_name=_("Diet Plan Name"), max_length=FieldConstants.MAX_NAME_LENGTH)
    category = models.ForeignKey(
        PlanCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="diet_plans"
    )
    plan_type = models.CharField(verbose_name=_("Plan Type"), choices=PLAN_TYPES, max_length=FieldConstants.MAX_VALUE_LENGTH)
    parent = models.ForeignKey(
                to="self",
                related_name="sub_categories",
                on_delete=models.PROTECT,
                blank=True, null=True
            )

    def clean(self) -> None:
        from django.core.exceptions import ValidationError

        # Main Category can't have parent
        if self.plan_type == PLAN_TYPES.main_category and self.parent is not None:
            raise ValidationError("Parent can't be specified for Main Category Plan Type")
        
        # Sub Category must have parent
        elif self.plan_type == PLAN_TYPES.sub_category and self.parent is None:
            raise ValidationError("Parent must be specified for Sub Category Plan Type")

        # Sub Category can't have 'self' as parent
        elif self.plan_type == PLAN_TYPES.sub_category and self.parent == self:
            raise ValidationError("Parent can't be the same plan")
        
        # Sub category can't have other Sub Category as parent
        elif self.plan_type == PLAN_TYPES.sub_category and self.parent.plan_type == PLAN_TYPES.sub_category:
            raise ValidationError("Sub category can't have other Sub Category as parent")
        
        return super().clean()

    class Meta:
        verbose_name = _("Diet Plan")
        verbose_name_plural = _("Diet Plans")
        unique_together = ['name', 'category']

    def __str__(self) -> str:
        return f"{self.name} - {self.category}"


class QuestionAnswer(BaseModel):
    diet_plan = models.ForeignKey(
                to=DietPlan,
                verbose_name=_("Diet Plan"),
                on_delete=models.CASCADE,
                related_name="question_answers"
            )
    
    question = models.CharField(max_length=FieldConstants.MAX_LENGTH)
    answer = models.TextField()

    class Meta:
        verbose_name = _("Question Answer")
        verbose_name_plural = _("Question Answers")

    def __str__(self) -> str:
        return f"{self.diet_plan} || {self.question}"


class Subscription(BaseModel):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(to=DietPlan, on_delete=models.PROTECT, related_name="subscribers")

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
        default=timezone.now() + timedelta(days=30),
        editable=False,
    )

    class Meta:
        verbose_name = _("Subscripton")
        verbose_name_plural = _("User Subscriptions")
    
    def __str__(self) -> str:
        return f'{self.user.full_name} - {self.plan.name} - {self.get_subscription_status_display()}'