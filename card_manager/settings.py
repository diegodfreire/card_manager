import os
from datetime import timedelta

import sentry_sdk

from unipath import Path
from decouple import config
from dj_database_url import parse as db_url
from sentry_sdk.integrations.django import DjangoIntegration


ROOT_DIR = Path(__file__).ancestor(3)
APPS_DIR = ROOT_DIR.child('card_manager')

SECRET_KEY = config(
    'SECRET_KEY',
    default="!!!SET SECRET_KEY!!!",
)

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", None),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*',
    cast=lambda v: [s.strip() for s in v.split(',')],
)

# Application definition

DJANGO_APPS = [
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
    'graphene_django',
    'elasticapm.contrib.django',
    'drf_yasg2',
    'django_filters',
    'corsheaders'
]

LOCAL_APPS = [
    'core',
]

AUTH_USER_MODEL = "core.Person"

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'card_manager.urls'

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
            ]
        },
    }
]

WSGI_APPLICATION = 'card_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url,
        default='postgres://card_manager:postgres@db:5432/card_manager'
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'  # noqa: E501
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
            '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.db.backends': {'level': 'DEBUG', 'handlers': ['console']}
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GRAPHENE = {
    'SCHEMA': 'core.schema.schema',
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

RABBITMQ_HOST = config("RABBITMQ_HOST", default="broker")
RABBITMQ_USER = config("RABBITMQ_USER", default="rabbit")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD", default="rabbit")
CONFIG_NAMEKO = {
    'AMQP_URI': f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}"
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTTokenUserAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

CORS_ORIGIN_ALLOW_ALL = True

SIMPLE_JWT = {
    "USER_ID_FIELD": "username",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "SIGNING_KEY": config("SIMPLE_JWT_KEY", default=SECRET_KEY),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
    }
}