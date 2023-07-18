"""
Django settings for Rqm project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from celery.schedules import crontab
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECRET_KEY = 'django-insecure-zw6(r)r4e_8keib-a$h2f-eojrw_=lues4fall1f(kqgvqn-0x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'
# DEBUG = False

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'userauth.User'

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

# Cors
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"


# Cloudinary settings
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
CLOUDINARY_URL = 'cloudinary://{api_key}:{api_secret}@{cloud_name}'

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Application definition
# Google Maps
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom
    'calls',
    'client',
    'userauth',
    # 'userprofile',

    # installed
    'rest_framework_simplejwt',
    'phonenumber_field',
    'django_ratelimit',
    'rest_framework',
    # 'googlemaps',
    'import_export',
    'corsheaders',
    'cloudinary',
    'drf_yasg',
    'celery',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # installed
    'django_ratelimit.middleware.RatelimitMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'rqm.urls'

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

WSGI_APPLICATION = 'rqm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'authentication.authentication.PinOrPasswordAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=100),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CELERY_broker_url = 'redis://localhost:6379/0'
# result_backend = 'redis://localhost:6379/0'

# Celery Beat Configuration
# CELERY_BEAT_SCHEDULE = {
#     'send_notification_5days': {
#         'task': 'Rqm.tasks.send_notification_5days',
#         'schedule': crontab(hour=0, minute=0),
#     },
#     'send_notification_3days': {
#         'task': 'Rqm.tasks.send_notification_3days',
#         'schedule': crontab(hour=0, minute=0),
#     },
#     'send_notification_1day': {
#         'task': 'Rqm.tasks.send_notification_1day',
#         'schedule': crontab(hour=0, minute=0),
#     },
#     'reset_subscription_task': {
#         'task': 'Rqm.tasks.reset_subscription_task',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }

# Celery configuration
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_BROKER_URL = 'redis://default:bmzkyITIlxNdfgi6VdfXHOQf7pIjmg1S@redis-15208.c270.us-east-1-3.ec2.cloud.redislabs.com:15208'
CELERY_RESULT_BACKEND = 'redis://default:bmzkyITIlxNdfgi6VdfXHOQf7pIjmg1S@redis-15208.c270.us-east-1-3.ec2.cloud.redislabs.com:15208'
CELERY_TASK_SERIALIZER = 'json'

# Redis configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://default:bmzkyITIlxNdfgi6VdfXHOQf7pIjmg1S@redis-15208.c270.us-east-1-3.ec2.cloud.redislabs.com:15208',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')


PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')