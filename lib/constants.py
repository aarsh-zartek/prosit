from enum import Enum
from django.utils.translation import gettext_lazy as _

from rest_framework import status


class FieldConstants:
    MAX_UID_LENGTH = 48
    MAX_LENGTH = 255
    MAX_NAME_LENGTH = 60
    MAX_VALUE_LENGTH = 24
    MAX_HEALTH_CODE_LENGTH = 8
    DATE_FORMAT = "%b %-d, %Y"
    FULL_DATE_FORMAT = "%B %d, %Y"
    DATE_TIME_FORMAT = f"{DATE_FORMAT} %-I:%M %p"
    FULL_DATE_TIME_FORMAT = f"{DATE_FORMAT} %I:%S:%M %p"


class SubscriptionIdentifier:
    ONE_MONTH_PLAN = "smart_plan_199"


class Device:
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


class SubscriptionPeriod:
    MONTHLY = "monthly"
    YEARLY = "yearly"


class EventType:
    TEST = "test"
    INITIAL_PURCHASE = "initial_purchase"
    NON_RENEWING_PURCHASE = "non_renewing_purchase"
    RENEWAL = "renewal"
    PRODUCT_CHANGE = "product_change"
    CANCELLED = "cancelled"
    BILLING_ISSUE = "billing_issue"
    SUBSCRIBER_ALIAS = "subscriber_alias"


class Environment:
    SANDBOX = "sandbox"
    PRODUCTION = "production"


class Store:
    PLAY_STORE = "play_store"
    APP_STORE = "app_store"
    STRIPE = "stripe"
    MAC_APP_STORE = "mac_app_store"
    PROMOTIONAL = "promotional"


class PeriodType:
    TRIAL = "trial"
    INTRO = "intro"
    NORMAL = "normal"
    PROMOTIONAL = "promotional"


class CancellationReason:
    UNSUBSCRIBE = "unsubscribe"
    BILLING_ERROR = "billing_error"
    DEVELOPER_INITIATED = "developer_initiated"
    PRICE_INCREASE = "price_increase"
    CUSTOMER_SUPPORT = "customer_support"
    UNKNOWN = "unknown"

class SubscriptionStatus:
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class AudioFormats(Enum):
    MP3 = "mp3"
    AAC = "aac"
    OGG = "ogg"
    WAV = "wav"

    @classmethod
    def all(audio_types):
        return [audio_type.value for audio_type in list(audio_types)]


class DocumentFormats(Enum):
    PDF = "pdf"

    @classmethod
    def all(document_types):
        return [document_type.value for document_type in list(document_types)]


POSITIVE_RESPONSES = [
    status.HTTP_200_OK,
    status.HTTP_201_CREATED,
    status.HTTP_202_ACCEPTED,
    status.HTTP_204_NO_CONTENT,
]

NEGATIVE_RESPONSES = [
    status.HTTP_400_BAD_REQUEST,
    status.HTTP_401_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN,
    status.HTTP_404_NOT_FOUND,
    status.HTTP_405_METHOD_NOT_ALLOWED,
    status.HTTP_418_IM_A_TEAPOT,
    status.HTTP_422_UNPROCESSABLE_ENTITY,
    status.HTTP_429_TOO_MANY_REQUESTS,
]
