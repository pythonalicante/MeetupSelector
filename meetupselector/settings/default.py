import os

from decouple import config
from django.db.models import ManyToManyField
from django.utils.translation import gettext_lazy as _

# --------------------------------------
# Typing
# --------------------------------------

# https://github.com/sbdchd/django-types#install
for cls in [ManyToManyField]:
    if hasattr(cls, "__class_getitem__"):
        raise Exception(f"Remove this class form the list: {cls}")
    cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type:ignore

# --------------------------------------
# General
# --------------------------------------

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = config("PROJECT_NAME", default="MeetUpSelector")


ALLOWED_HOSTS: list[str] = []

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS: list[str] = [
    "corsheaders",
    "django_celery_beat",
    "django_filters",
]

OUR_APPS = [
    "meetupselector.user",
    "meetupselector.talks",
    "meetupselector.proposals",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OUR_APPS


MIDDLEWARE = [
    # Web security
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # Auth
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Regular
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "meetupselector.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "string_if_invalid": '<< MISSING VARIABLE "%s" >>' if DEBUG else "",
        },
    }
]

WSGI_APPLICATION = "meetupselector.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", ""),  # noqa
        "USER": os.environ.get("POSTGRES_USER", "postgres"),  # noqa
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),  # noqa
        "HOST": os.environ.get("POSTGRES_HOST", ""),  # noqa
        "PORT": os.environ.get("POSTGRES_PORT", ""),
        "TEST": {
            "NAME": "test_wbsairback_database",
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User Model
AUTH_USER_MODEL = "user.User"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("es", _("spanish")),
    ("en", _("english")),
]
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR + "/locale/",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = "/app/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = "/app/media/"
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = config(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)


# Our custom config
CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "debug": {
            "class": "logging.StreamHandler",
            "formatter": "ultra-verbose",
        },
    },
    "formatters": {
        "ultra-verbose": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(pathname)s:%(funcName)s:%(lineno)d] -> %(message)s",  # noqa
            "style": "%",
        },
        "verbose": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] -> %(message)s",  # noqa
            "style": "%",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "meetupselector": {
            "handlers": ["debug"],
            "level": os.getenv("LOGGER_LEVEL", "DEBUG"),
            "propagate": False,
        },
    },
}

# Emails

# Global switch
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# e.g., info@here.com
DEFAULT_FROM_EMAIL = config("EMAIL_FROM_EMAIL", default=None)
CONTACT_EMAIL = config("EMAIL_CONTACT_EMAIL", default=None)

# SMTP config
EMAIL_HOST = config("SMTP_HOST", default="")
EMAIL_PORT = config("SMTP_PORT", default=25, cast=int)
EMAIL_HOST_USER = config("SMTP_USER", default=None)
EMAIL_HOST_PASSWORD = config("SMTP_PASSWORD", default=None)
EMAIL_USE_TLS = config("SMTP_TLS", default=False, cast=bool)


# CELERY STUFF
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = config("CELERY_BROKER_URL", default="redis://redis:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

API_VERSION = "alpha"
API_NAMESPACE = f"api-{API_VERSION}"
