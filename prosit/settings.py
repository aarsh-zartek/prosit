"""
Django settings for prosit project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from environ import environ
import os

import logging.config
from django.utils.log import DEFAULT_LOGGING

from lib.constants import FieldConstants

env = environ.Env()
environ.Env.read_env()

env.escape_proxy = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

DOMAIN = env.str('DOMAIN')
DOMAIN_IP = env.str('DOMAIN_IP')
TESTING_DOMAIN = env.str('TESTING_DOMAIN')

ALLOWED_HOSTS = [DOMAIN, DOMAIN_IP, TESTING_DOMAIN]


# Application definition

DJANGO_APPS = [
    # Must be added before `django.contrib.admin`
    'jazzmin', # Custom Admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'django_celery_beat',
    'django_celery_results',
    'drf_yasg',
    'corsheaders',
    'phonenumber_field',
    'ckeditor',
]

LOCAL_APPS = [
    'apps.firebase.apps.FirebaseConfig',
    'apps.core.apps.CoreConfig',
    'apps.users.apps.UsersConfig',
    'apps.plan.apps.PlanConfig',
    'apps.about.apps.AboutConfig',
    'apps.notification.apps.NotificationConfig',
    'apps.subscriptions.apps.SubscriptionsConfig',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'apps.core.exceptions.CustomExceptionMiddleware',
]

ROOT_URLCONF = 'prosit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'prosit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

# 'default': env.db_url()

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static/'),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media Files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Loggers
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()
LOG_FILE_NAME = os.path.join(BASE_DIR, "logs/prosit.log")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '.cache',
    }
}

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # Add Handler for Sentry for `warning` and above
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_NAME,
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'default',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
        # Our application code
        'apps.firebase': {
            'level': LOGLEVEL,
            'handlers': ['console', 'file'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'apps.plan': {
            'level': LOGLEVEL,
            'handlers': ['console', 'file'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # # Prevent noisy modules from logging to Sentry
        # 'noisy_module': {
        #     'level': 'ERROR',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})


# CORS
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1:8000',
#     'http://localhost:8000',
#     'https://*.ngrok.io',
# )

# CSRF_TRUSTED_ORIGINS = ['https://*.ngrok.io','https://*.127.0.0.1']

# Rest Framework Config - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.firebase.authentication.FirebaseAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'apps.core.renderers.CustomAPIRenderer',
    ),
    # "DATE_TIME_FORMAT": FieldConstants.FULL_DATE_TIME_FORMAT
}

FIREBASE_CONFIG = {
    "FIREBASE_SERVICE_ACCOUNT": env.str("FIREBASE_SERVICE_ACCOUNT"),
    "FIREBASE_WEBAPP_CONFIG": env.str("FIREBASE_WEBAPP_CONFIG"),
}

REVENUE_CAT_API_KEY = env.str("REVENUE_CAT_API_KEY")

# Djoser Config
DJOSER = {
    'SERIALIZERS': {
        'current_user': 'apps.users.serializers.UserSerializer',
        'user': 'apps.users.serializers.UserSerializer',
    },
}

JAZZMIN_SETTINGS = {
    "site_brand": "Prosit Health",
    "site_icon": "icon.png",
    "site_logo": "prosit-logo.png",
    "welcome_sign": "Welcome to Prosit Admin Panel",

    "icons": {
        "authtoken.tokenproxy": "fas fa-coins",
        
        "about.company": "fas fa-building",
        "about.faq": "fas fa-meh",

        "notification.notification": "fas fa-bell",
        
        "plan.dietplan": "fas fa-calendar-alt",
        "plan.plantype": "fas fa-stream",
        "plan.plancategory": "fas fa-list",
        "plan.questionanswer": "fas fa-question",
        "plan.subscription": "fas fa-rupee-sign",

        "users.user": "fas fa-users",
        "users.profile": "fas fa-id-card",
        "users.userhealthreport": "fas fa-file-medical",
        "users.dailyactivity": "fas fa-calendar-day",

        "django_celery_beat.clockedschedule": "fas fa-alarm-clock",
        "django_celery_beat.crontabschedule": "fas fa-stopwatch",
        "django_celery_beat.intervalschedule": "fas fa-watch",
        "django_celery_beat.periodictask": "fas fa-chess-clock",
        "django_celery_beat.solarschedule": "fas fa-solar-system",

        "django_celery_results.groupresult": "fas fa-poll",
        "django_celery_results.taskresult": "fas fa-tasks",
    },

    # "changeform_format": "vertical_tabs"
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-gray-dark navbar-dark",
    "theme": "litera",
    #00a68c

    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success"
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Prosit',
        'toolbar_Prosit': [
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
            },
            {
                'name': 'paragraph',
                'items': [
                    'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'
                ]
            },
            {
                'name': 'clipboard',
                'items': [
                    'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'
                ]
            },
            {
                'name': 'styles',
                'items': ['Styles', 'Format', 'Font', 'FontSize']
            },
            '/',  # put this to force next toolbar on new line
            {
                'name': 'preview-maximize', 'items': [
                    # put the name of your editor.ui.addButton here
                    'Preview',
                    'Maximize',
                ]
            },
        ]
    },
}


# Celery Configuration

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

## Celery Results Configuration

CELERY_RESULT_BACKEND = 'django-db'
