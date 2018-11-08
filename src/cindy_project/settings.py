import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
VIRTUALENV_DIR = os.environ.get('VIRTUAL_ENV')
BIN_FOLDER = os.path.join(VIRTUALENV_DIR, 'bin')
SECRET_KEY = os.getenv('CINDY_SECRET_KEY')

DEBUG = 'CINDY_DEBUG' in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

SITE_ID = 1


# Application definition

LIBRARY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'taggit',
    'compressor',
    'material.theme.teal',
    'material'
]

APPS = [
    'cindy',
    'web'
    ]

INSTALLED_APPS = tuple(LIBRARY_APPS + APPS)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
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


ROOT_URLCONF = 'cindy_project.urls'

WSGI_APPLICATION = 'cindy_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('CINDY_DATABASE_ENGINE'),
        'HOST': os.getenv('CINDY_DATABASE_HOST'),
        'PORT': os.getenv('CINDY_DATABASE_PORT', 5432),
        'NAME': os.getenv('CINDY_DATABASE_NAME'),
        'USER': os.getenv('CINDY_DATABASE_USER'),
        'PASSWORD': os.getenv('CINDY_DATABASE_PASSWORD')
    }
}


MESSAGE_BROKER = {
    'URL': os.getenv('CINDY_BROKER_URL'),
    'USE_SSL': bool(int(os.getenv('CINDY_BROKER_USE_SSL', 0))),
    'QUEUE_NAME': os.getenv('CINDY_BROKER_QUEUE_NAME', 'cindy_project')
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

STATIC_URL = os.getenv('CINDY_STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('CINDY_STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', '{} {{infile}} {{outfile}}'.format(os.path.join(BIN_FOLDER, 'sassc'))),
)

# Media files (user generated content)
MEDIA_ROOT = os.getenv('CINDY_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))


# REST API Configuration
REST_RENDERERS = [
    'rest_framework.renderers.JSONRenderer'
]

if DEBUG:
    REST_RENDERERS.append('rest_framework.renderers.BrowsableAPIRenderer')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': tuple(REST_RENDERERS)
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Taggit configuration
TAGGIT_CASE_INSENSITIVE = True
