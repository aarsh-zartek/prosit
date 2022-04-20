from django.conf import settings

FIREBASE_CONFIG = getattr(set, "FIREBASE_CONFIG", {})

# Firebase
FIREBASE_CONFIG.setdefault("FIREBASE_SERVICE_ACCOUNT", settings.FIREBASE_CONFIG["FIREBASE_SERVICE_ACCOUNT"])
FIREBASE_CONFIG.setdefault("FIREBASE_WEBAPP_CONFIG", settings.FIREBASE_CONFIG["FIREBASE_WEBAPP_CONFIG"])

# User model
FIREBASE_CONFIG.setdefault("USER_MODEL", settings.AUTH_USER_MODEL)

# settings.INSTALLED_APPS += ['phonenumber_field']