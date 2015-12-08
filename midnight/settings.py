"""
Django settings for midnight project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from .settings_local import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEME_NAME = "demo"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6fqr9$#ab!pwrw7yamrktl87e^@bc=fmujwr08s^o^led5^8j'

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'ckeditor',
    'sorl.thumbnail',
    'bootstrap_pagination',
    'django_assets',
    'bootstrapform',
    'captcha',
    'registration',
    'precise_bbcode',
    'haystack',
    'midnight_main',
    'midnight_news',
    'midnight_banners',
    'midnight_catalog',
) + ADDITIONAL_APPS

# User model

AUTH_USER_MODEL = 'midnight_main.AppUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'midnight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'midnight/templates/'+THEME_NAME,
            'midnight/templates/common',
        ],
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

WSGI_APPLICATION = 'midnight.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
  BASE_DIR + '/midnight/locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "www", "bower_components"),
    os.path.join(BASE_DIR, "www", "themes", THEME_NAME),
)

# Media storage

MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')
MEDIA_URL = '/media/'

# Assets

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

# Captcha

CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)

# Registration

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# Grapelli

GRAPPELLI_INDEX_DASHBOARD = 'midnight.dashboard.CustomIndexDashboard'

GRAPPELLI_ADMIN_TITLE = 'Midnight CMS'


# CKeditor settings

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')

CKEDITOR_CONFIGS = {
    'default': {
        'filebrowserBrowseUrl': '/admin/filebrowser/browse?pop=3'
    }
}

# Sorl thumbnail (resize)

THUMBNAIL_COLORSPACE = None

THUMBNAIL_PRESERVE_FORMAT = True

# Haystack search

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
