from pathlib import Path
from os import getenv

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / "django.env")

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

DEBUG = getenv("DJANGO_DEBUG") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "www.asciiforever.net"]


# Application definition

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apps.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": (BASE_DIR / "my.cnf").as_posix(),
        },
    }
}


# Auth

AUTH_USER_MODEL = "core.User"

LOGIN_URL = "/users/sign_in"


# Password validation

validators = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
]
AUTH_PASSWORD_VALIDATORS = [{"NAME": validator} for validator in validators]


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Files

STATIC_ROOT = "/var/www/www.asciiforever.net/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = "/var/www/www.asciiforever.net/media/"
MEDIA_URL = "/media/"

# Default model id

DEFAULT_AUTO_FIELD="django.db.models.AutoField"
