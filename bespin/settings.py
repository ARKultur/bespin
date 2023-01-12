"""
Django settings for bespin project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import string
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_API_KEY']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@arkultur.creative-rift.com'

TRENCH_AUTH = {
    "USER_MFA_MODEL": "trench.MFAMethod",
    "USER_ACTIVE_FIELD": "is_active",
    "BACKUP_CODES_QUANTITY": 5,
    "BACKUP_CODES_LENGTH": 12,
    "BACKUP_CODES_CHARACTERS": (string.ascii_letters + string.digits),
    "SECRET_KEY_LENGTH": 32,
    "DEFAULT_VALIDITY_PERIOD": 30,
    "CONFIRM_DISABLE_WITH_CODE": False,
    "CONFIRM_BACKUP_CODES_REGENERATION_WITH_CODE": True,
    "ALLOW_BACKUP_CODES_REGENERATION": True,
    "ENCRYPT_BACKUP_CODES": True,
    "APPLICATION_ISSUER_NAME": "ARKultur",
    "MFA_METHODS": {
        "email": {
            "VERBOSE_NAME": "email",
            "VALIDITY_PERIOD": 60 * 5,
            "HANDLER": "trench.backends.basic_mail.SendMailMessageDispatcher",
            "SOURCE_FIELD": "auth.email",
            "EMAIL_SUBJECT": "Your verification code",
            "EMAIL_PLAIN_TEMPLATE": "trench/backends/email/code.txt",
            "EMAIL_HTML_TEMPLATE": "trench/backends/email/code.html",
        },
        "sms_api": {
            "VERBOSE_NAME": "sms_api",
            "VALIDITY_PERIOD": 60,
            "HANDLER": "trench.backends.sms_api.SMSAPIMessageDispatcher",
            "SOURCE_FIELD": "auth.phone_number",
            "SMSAPI_ACCESS_TOKEN": os.environ.get('TWILIO_API_KEY'),
            "SMSAPI_FROM_NUMBER": os.environ.get('TWILIO_PHONE_NUMBER'),
        },
        "app": {
            "VERBOSE_NAME": "app",
            "VALIDITY_PERIOD": 30,
            "USES_THIRD_PARTY_CLIENT": True,
            "HANDLER": "trench.backends.application.ApplicationMessageDispatcher",
        }
    }
}

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'FR'
PHONENUMBER_DEFAULT_FORMAT = 'E164'

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'drf_yasg',
    'trench',
    "phonenumber_field",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bespin.urls'

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

WSGI_APPLICATION = 'bespin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if os.environ.get('PRODUCTION', '0') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': os.environ.get('POSTGRES_PORT'),
        }
    }
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
    DEBUG = False
    ALLOWED_HOSTS = ['server', 'localhost']
elif os.environ.get('TEST') and os.environ.get('TEST')  == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'bespin',
            'USER': os.environ.get('USER'),
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    SECRET_KEY = 'django-insecure-mdvq2h0e3!@5edgf)5c2qt@cin6m3(3n8f=5gi6qdy207oi-p)'
    DEBUG = True
    ALLOWED_HOSTS = ['*']
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'bespin',
            'USER': os.environ.get('USER'),
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    SECRET_KEY = 'django-insecure-mdvq2h0e3!@5edgf)5c2qt@cin6m3(3n8f=5gi6qdy207oi-p)'
    DEBUG = True
    ALLOWED_HOSTS = ['*']


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

AUTH_USER_MODEL = "api.auth"
AUTHENTICATION_BACKENDS = [
    'api.backends.EmailBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    }

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
