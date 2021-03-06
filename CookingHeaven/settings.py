import os
from pathlib import Path

import cloudinary
from django.urls import reverse_lazy

from CookingHeaven.utils import is_production, is_test

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'sk')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'Development')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1 localhost').split(' ')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'CookingHeaven.main',
    'CookingHeaven.accounts',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'CookingHeaven.middlewares.HandleExceptionMiddleware',
]

ROOT_URLCONF = 'CookingHeaven.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'CookingHeaven.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'NAME': os.getenv('DB_NAME', 'cooking_heaven_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', '1123QwER'),

    }

}

AUTH_PASSWORD_VALIDATORS = []
if is_production():
    AUTH_PASSWORD_VALIDATORS.extend([
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
    ])

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR /'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGGING_LEVEL = 'DEBUG'

if is_production():
    LOGGING_LEVEL = 'INFO'
elif is_test():
    LOGGING_LEVEL = 'CRITICAL'

LOGS_DIR = BASE_DIR / 'logs'

try:
    os.mkdir(LOGS_DIR)
except:
    pass





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOGGING_LEVEL,
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': LOGGING_LEVEL,
            'filename': LOGS_DIR / 'Log.txt',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': LOGGING_LEVEL,
        },
    },
}


AUTH_USER_MODEL = 'accounts.CookingHeavenUser'

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', None),
    api_key=os.getenv('CLOUDINARY_API_KEY', None),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', None),
)
