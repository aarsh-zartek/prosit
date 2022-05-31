from enum import Enum
from django.utils.translation import gettext_lazy as _


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
