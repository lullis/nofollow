# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('NOFOLLOW_SECRET_KEY')

DEBUG = 'NOFOLLOW_NODEBUG' not in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

LIBRARY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'taggit',
]

APPS = [
    'core'
    ]

INSTALLED_APPS = tuple(LIBRARY_APPS + APPS)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]


ROOT_URLCONF = 'nofollow.urls'

WSGI_APPLICATION = 'nofollow.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('NOFOLLOW_DATABASE_ENGINE'),
        'HOST': os.getenv('NOFOLLOW_DATABASE_HOST'),
        'PORT': os.getenv('NOFOLLOW_DATABASE_PORT', 5432),
        'NAME': os.getenv('NOFOLLOW_DATABASE_NAME'),
        'USER': os.getenv('NOFOLLOW_DATABASE_USER'),
        'PASSWORD': os.getenv('NOFOLLOW_DATABASE_PASSWORD')
    }
}


MESSAGE_BROKER = {
    'URL': os.environ.get('NOFOLLOW_BROKER_URL'),
    'USE_SSL': bool(int(os.environ.get('NOFOLLOW_BROKER_USE_SSL', 0)))
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


# Media files (user generated content)
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))


# REST API Configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Taggit configuration
TAGGIT_CASE_INSENSITIVE = True
