"""
Django settings for careweb project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.management.utils import get_random_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "q7(#m#a%md&pg(i^cc+u(+t&0*nfbn2omp)yu2-u!8a3a6mzbj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "futurecare.ng",
    "futurecare.com.ng",
    "futurecare.everyday.com.ng",
    "localhost",
    "174.138.47.148",
    "192.168.8.100",
    "192.168.1.4",
    "127.0.0.1",
    "167.172.156.45",
]

# Email settings
# EMAIL_BACKEND = "postmarker.django.EmailBackend"
EMAIL_BACKEND = "post_office.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@futurecare.ng"

POST_OFFICE = {"BACKENDS": {"default": "postmarker.django.EmailBackend",}}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

# Application definition

INSTALLED_APPS = [
    "constance",
    "baton",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # local
    "client.apps.ClientConfig",
    "core.apps.CoreConfig",
    "ranger.apps.RangerConfig",
    "location.apps.LocationConfig",
    "provider.apps.ProviderConfig",
    "payment.apps.PaymentConfig",
    "subscription.apps.SubscriptionConfig",
    "sms.apps.SmsConfig",
    # 3rd party
    "post_office",
    "baton.autodiscover",
    "widget_tweaks",
    "crispy_forms",
    "constance.backends.database",
    "rest_framework",
    "drf_yasg",
    "simple_history",
    # "easy_select2"
    # "easyaudit",
]

CONSTANCE_CONFIG = {
    "AGENT_COMMISSION": (5, "Commission for Agents as a percentage of subscription"),
    "CLIENT_DEFAULT_PASSWORD": (
        "Qwerty123",
        "Default password for clients registered by rangers.",
    ),
    "LEN_VERIFICATION_CODE": (5, "Length of verification code for new users"),
    "CLIENT_LIMIT": (2000, "Limit to notify users"),
    "CLIENT_LIMIT_RECEIVERS": ("", "List of emails to be notified of client limit"),
}

# DJANGO_EASY_AUDIT_UNREGISTERED_URLS_EXTRA = [
#    r"^/baton/app-list-json/",
#    r"/favicon.png$",
# ]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware"
    # "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]

ROOT_URLCONF = "careweb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "ranger.context_processors.ranger_balance",
            ],
        },
    },
]

WSGI_APPLICATION = "careweb.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Session
SESSION_COOKIE_AGE = 3000

# login
LOGIN_URL = "/client/login/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "otherstatic"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

PAYSTACK_PUBLIC_KEY = ""
PAYSTACK_SECRET_KEY = ""

BATON = {
    "SITE_HEADER": "FUTURECARE",
    "SITE_TITLE": "FUTURECARE",
    "INDEX_TITLE": "Site administration",
    "CONFIRM_UNSAVED_CHANGES": True,
    "COPYRIGHT": "Futureview Solutions",
    "POWERED_BY": "Futureview",
    "SUPPORT_HREF": "http://futurecare.everyday.com.ng",
}

HASHID_FIELD_ALLOW_INT_LOOKUP = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(asctime)s %(message)s"},},
    "handlers": {
        "client_logfile": {
            "formatter": "simple",
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/client.log"),
        },
        "ranger_logfile": {
            "formatter": "simple",
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/ranger.log"),
        },
        "payment_logfile": {
            "formatter": "simple",
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/payment.log"),
        },
    },
    "loggers": {
        "client": {"handlers": ["client_logfile"], "level": "INFO", "propagate": True,},
        "ranger": {"handlers": ["ranger_logfile"], "level": "INFO", "propagate": True,},
        "core": {"handlers": ["ranger_logfile"], "level": "INFO", "propagate": True,},
        "payment": {
            "handlers": ["payment_logfile"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

FILE_UPLOAD_HANDLERS = (
    "django_excel.ExcelMemoryFileUploadHandler",
    "django_excel.TemporaryExcelFileUploadHandler",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    # 'EXCEPTION_HANDLER': 'log_manager.views.exception_handler'
}
HASHID_FIELD_SALT = "v3m*lx71+z51ymv1hb=ts4uj%=34*r@4=y3ajz(+!&4!=r8nv^"

IS_TEST_SERVER = False

if IS_TEST_SERVER:
    try:
        from .test_settings import *
    except ImportError:
        pass

try:
    from .local_settings import *
except ImportError:
    pass
