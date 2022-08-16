from django.core.validators import FileExtensionValidator as FEV
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel
from apps.users.models import User

from lib.constants import FieldConstants, DocumentFormats

# Create your models here.


class Company(BaseModel):

    home_page_title = models.TextField(verbose_name=_("Home Page Title"))
    home_page_text = models.TextField(verbose_name=_("Home Page Text"))

    contact_number = PhoneNumberField(verbose_name=_("Company Contact Number"))
    about_the_company = models.TextField(verbose_name=_("About The Company"))
    address = models.TextField(verbose_name=_("Company Address"))
    
    terms_and_conditions = models.TextField(verbose_name=_("Terms And Conditions"))
    privacy_policy = models.TextField(verbose_name=_("Privacy Policy"))

    banner_title = models.TextField(verbose_name=_("Banner"))
    banner_text = models.TextField(verbose_name=_("Banner Text"))

    # image = models.ImageField(verbose_name=_("Image"))

    stop_plan_pdf = models.FileField(
                verbose_name=_("Stop Plan PDF"),
                upload_to="stop_plan/",
                validators=[
                    FEV(allowed_extensions=DocumentFormats.all())
                ],
                blank=True,
                null=True
            )

    class Meta:
        verbose_name = _("Company Config")
        verbose_name_plural = _("Company Configuration")
    
    def __str__(self) -> str:
        return f"{self.home_page_title}"


class FAQ(BaseModel):

    company = models.ForeignKey(to=Company, related_name="faqs", on_delete=models.CASCADE)
    question = models.CharField(verbose_name=_("Question"),max_length=FieldConstants.MAX_LENGTH)
    answer = models.TextField()

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
    
    def __str__(self):
        return self.company.__str__()


class ContactForm(BaseModel):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)

    email = models.EmailField()
    phone_number = PhoneNumberField()
    message = models.TextField()
    
    class Meta:
        verbose_name = _("Contact Form")
        verbose_name_plural = _("Contact Forms")
