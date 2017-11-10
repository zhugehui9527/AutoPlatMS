"""
Django settings for AutoPlatMS project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g2b0(p=0e%kvqqha#gmqu!u_o0u8#vlhpzzinh5jr6(2@g0p-h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.180.144.2','127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'navi',
    'cmdb',
    'case',
    'rest_framework',
]

# AUTH_USER_MODEL = 'users.User'
# USERS_REGISTRATION_OPEN = True
#
# USERS_VERIFY_EMAIL = True
#
# USERS_AUTO_LOGIN_ON_ACTIVATION = True
#
# USERS_EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3
#
# # Specifies minimum length for passwords:
# USERS_PASSWORD_MIN_LENGTH = 5
#
# # Specifies maximum length for passwords:
# USERS_PASSWORD_MAX_LENGTH = None
#
# # the complexity validator, checks the password strength
# USERS_CHECK_PASSWORD_COMPLEXITY = True
#
# USERS_SPAM_PROTECTION = False  # important!
#
# #  ---------------------------------------------------------
# #  Email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'smtp.tuweizhong.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'mail@tuweizhong.com'
# EMAIL_HOST_PASSWORD = 'xxxx'
# DEFAULT_FROM_EMAIL = 'mail@tuweizhong.com'
# #  ---------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AutoPlatMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'AutoPlatMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/statics/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'statics')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "statics").replace('\\', '/'),

)

# STATICFILES_FINDERS = (
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder"
# )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

AUTH_USER_MODEL = 'accounts.UserInfo'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
