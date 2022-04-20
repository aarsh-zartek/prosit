import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from lib.constants import FieldConstants

from .managers import UserManager


class AbstractFirebaseUser(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(unique=True, default=uuid.uuid1, max_length=FieldConstants.MAX_UID_LENGTH)
    first_name = models.CharField(
        verbose_name="First Name",
        max_length=FieldConstants.MAX_NAME_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="Last Name",
        max_length=FieldConstants.MAX_NAME_LENGTH,
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(
        verbose_name="phone_number",
        unique=True,
        error_messages={
            "unique": "A user with this phone number already exists",
        },
    )
    email = models.EmailField(
        verbose_name="Email Address",
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": "A user with this email already exists"},
    )
    is_staff = models.BooleanField(
        verbose_name="Staff Status",
        default=False,
        help_text="Designate whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        verbose_name="active",
        default=True,
        help_text="Designates whether this use should be treated as active"
        "unselect this instead of deleting accounts (soft delete)",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "uid"
    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        abstract = True

    def get_username(self):
        return f"{self.identifier}"

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def full_name(self):
        return f'{self.first_name} - {self.last_name}'

    @property
    def identifier(self):
        return self.full_name or self.phone_number or self.email or self.uid


class FirebaseUser(AbstractFirebaseUser):
    class Meta(AbstractFirebaseUser.Meta):
        swappable = "AUTH_USER_MODEL"
