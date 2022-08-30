"""
Django settings for servermanager project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os, sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h^(ah*cpz3@wenhjw7$!k#ags8^k*&$8=jk3%s4_%bw*dph+d("

# SECURITY WARNING: don't run with debug turned on in production!
RUNNING_DEVSERVER = len(sys.argv) > 1 and sys.argv[1] == 'runserver'
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

PGPASSWORD= os.environ.get('PGPASSWORD','jqkNlGwwDLN2xC7L')
PGUSER = os.environ.get('PGUSER','postgres')
PGHOST = os.environ.get('PGHOST','localhost')
DEBUG=os.environ.get('DEBUG','False') == 'True'


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "opentasites.apps.OpentasitesConfig",
    "django_json_widget",
    "accounts",
    'rest_framework',
    "friendship",
    "crispy_forms",
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

ROOT_URLCONF = "servermanager.urls"

TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

WSGI_APPLICATION = "servermanager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASE_ROUTERS = ['servermanager.routers.AuthRouter']
DB_FOR_MANAGER = "managerdefault1"
DATABASES =  {
   'default' : {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': DB_FOR_MANAGER,
      'USER': PGUSER,
      'PASSWORD': PGPASSWORD,
      'HOST': PGHOST,
      'PORT': 5432,
    },
   'opentasites' : {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'opentasites',
      'USER': PGUSER,
      'PASSWORD': PGPASSWORD,
      'HOST': PGHOST,
      'PORT': 5432,
    }
 }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

NO_AUTH_PASSWORD_VALIDATORS = [
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Europe/Copenhagen'
USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "deploystatic")
ALLOWED_HOSTS = ['*']
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
CRISPY_TEMPLATE_PACK = 'bootstrap4'
