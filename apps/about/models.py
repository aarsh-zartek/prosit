from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel

from lib.constants import FieldConstants

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
        