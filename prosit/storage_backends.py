from fnmatch import fnmatch
from storages.backends.s3boto3 import S3Boto3Storage

# Create your storages here.

WHITELIST = ['admin/css/widgets.css', 'admin/css/fonts.css', 'admin/fonts/*.woff', 'admin/img/*.svg']


class StaticStorage(S3Boto3Storage):
    location = "static"
    defaul_acl = "private"


class MediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "private"
    querystring_auth = True

    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)

        if any(fnmatch(name, pattern) for pattern in WHITELIST):
            params["ACL"] = "public-read"

        return params
