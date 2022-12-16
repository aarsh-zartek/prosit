from rest_framework import serializers
from rest_framework.settings import api_settings

from prosit.settings import AWS_STORAGE_BUCKET_NAME

from lib.utils import generate_presigned_url, get_object_name


class AWSS3PresignedURLFileField(serializers.FileField):
    """
    Custom FileField that returns AWS presigned URL to share an S3 object
    instead of media url for S3 objects that don't have public access
    """

    def to_representation(self, value):
        try:
            if not value:
                return None

            use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
            if use_url:
                url = generate_presigned_url(
                    bucket=AWS_STORAGE_BUCKET_NAME,
                    obj=get_object_name(
                        file=value
                    )
                )
                return url

            return value.name

        except Exception:
            return super().to_representation(value)
