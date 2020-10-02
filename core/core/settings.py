"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'app/static/app/js', 'serviceworker.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a&2f8e4$^j)-##yb+rn!73$@_n1ugp8dhkx*aqjwkmgs2xgmif'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '139.59.79.72', "a3d9d88f0011.ngrok.io"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',
    'tinymce',
    'phonenumber_field',
    'crispy_forms',
    'bootstrap4',
    'bootstrap_modal_forms',

    'paytm',
    'paywix',
    'app',
    'blog',
    'dashboard',


]
# EMAIL_BACKEND ='django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'phanigoud123@gmail.com'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# EMAIL_PORT = 1025

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'mekapotulaphani@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'phanigoud123@gmail.com'
EMAIL_HOST_PASSWORD = '8125997699'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydata',
        'USER': 'postgres',
        'PASSWORD': 'sanjayjanu@1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = 'app.User'

LOGIN_REDIRECT_URL = 'app:home'
LOGOUT_REDIRECT_URL = 'app:home'
LOGIN_URL = 'app:signin'

PAYTM_COMPANY_NAME = "Farmway Organics"  # For representation purposes
PAYTM_INDUSTRY_TYPE_ID = "Retail"  # For staging environment
PAYTM_CHANNEL_ID = "WEB"
PAYTM_MERCHANT_KEY = "Vv5M5Iu9b4Yr5&mv"
PAYTM_MERCHANT_ID = "cxgUTw88628774174098"
PAYTM_CALLBACK_URL = "http://localhost:8000/response/"  # Hardcode
PAYTM_WEBSITE = "WEBSTAGING"
PAYTM_PAYMENT_GATEWAY_URL = "https://securegw-stage.paytm.in/order/process"
PAYTM_TRANSACTION_STATUS_URL = "https://securegw-stage.paytm.in/order/status"

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'IN'


PAYU_CONFIG = {
        "merchant_key": "5cBJaTwT",
        "merchant_salt": "4C2gwCohCQ",
        "mode": "test",
        "success_url": "http://127.0.0.1:8000/payu_success/",
        "failure_url": "http://127.0.0.1:8000/failure/"
  }