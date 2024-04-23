from pathlib import Path
import os
from decouple import config as env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ON_VPS=env("ON_VPS")=="true"

SECRET_KEY = env("SECRET_KEY")

DEBUG = not ON_VPS

if ON_VPS:
    ALLOWED_HOSTS = ['184.94.215.214']
else:
    ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "app_authentication",
    "bank_management",
    'widget_tweaks',
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

ROOT_URLCONF = 'banking_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"banking_system/templates")],
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

WSGI_APPLICATION = 'banking_system.wsgi.application'



if ON_VPS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"), 
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("LOCAL_DB_NAME"),
            'USER': env("LOCAL_DB_USER"),
            'PASSWORD': env("LOCAL_DB_PASSWORD"),
            'HOST': env("LOCAL_DB_HOST"),
            'PORT': '5432',
        }
    }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'app_authentication.User'

STATIC_URL = '/static/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'banking_system/static')
]
STATIC_ROOT = "/home/pynabyte/static_root_directory/static_root_banking_application" if ON_VPS else ''

# Login
LOGIN_REDIRECT_URL = 'loans'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'authentication/login'

EMAIL_BACKEND = env("EMAIL_BACKEND") 
EMAIL_HOST = env("EMAIL_HOST") 
EMAIL_HOST_USER = env("EMAIL_HOST_USER") 
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS") 
EMAIL_PORT = env("EMAIL_PORT") 