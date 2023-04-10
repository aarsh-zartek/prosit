from datetime import datetime, timedelta
import logging
import os
import uuid

from django.utils import timezone

from botocore.exceptions import BotoCoreError
import boto3

logger = logging.getLogger(__name__)


def get_diet_plan_instruction_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f"{instance.name}/instruction/{file}"
    return file_path


def get_preparation_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f"{instance.name}/preparation/{file}"
    return file_path


def get_diet_plan_image_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f"{instance.name}/{file}"
    return file_path


def get_user_health_image_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f"{instance.user.uid}/health_reports/{file}"
    return file_path


def get_profile_picture_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f"{instance.uid}/profile_picture/{file}"
    return file_path


def one_month_from_today(days=30) -> datetime:
    return timezone.now() + timedelta(days=days)


def last_month_from_today(days=30) -> datetime:
    return timezone.now() - timedelta(days=days)


def get_object_name(file) -> str:
    return os.path.join(file.storage.location, file.name)


def generate_presigned_url(bucket: str, obj, expiration=3600) -> str:
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html
    """
    Generate a Presigned URL to share an S3 object

    Args:
        bucket (str): Bucket Name
        obj (Any): Object Name
        expiration (int, optional): Expiration time of URL in seconds. Defaults to 3600.

    Returns:
        str: Presigned URL
    """
    url = None
    try:
        client = boto3.client("s3")
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": obj},
            ExpiresIn=expiration,
        )
    except BotoCoreError as err:
        logger.exception(err)

    return url
