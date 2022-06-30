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


class DietPlanCategory:
    MALYALAM_DIET = "malayalam_diet"


class DietPlanType:
    WEIGHT_LOSS_PLAN = "weight_loss_plan"
    WEIGHT_GAIN_PLAN = "weight_gain_plan"
    GYM_FITNESS_PLAN = "gym_fitness_plan"
    BALANCED_DIET_PLAN = "balanced_diet_plan"


class Subscription:
    class PaymentMethod:
        WALLET = "wallet"
        CREDIT_CARD = "credit_card"
        DEBIT_CARD = "debit_card"
        UPI = "upi"
        NET_BANKING = "net_banking"
    
    class PaymentStatus:
        PENDING = "pending"
        PROCESSING = "processing"
        SUCCESSFUL = "successful"
        FAILED = "failed"
        REJECTED = "rejected"

    class SubscriptionStatus:
        INACTIVE = "inactive"
        ACTIVE = "active"
        EXPIRED = "expired"
    

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
    status.HTTP_204_NO_CONTENT
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
