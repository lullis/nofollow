import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
VIRTUALENV_DIR = os.environ.get('VIRTUAL_ENV')
BIN_FOLDER = os.path.join(VIRTUALENV_DIR, 'bin')
SECRET_KEY = os.getenv('NOFOLLOW_SECRET_KEY')

DEBUG = 'NOFOLLOW_DEBUG' in os.environ

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
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'taggit',
    'compressor',
    'material.theme.teal',
    'material'
]

APPS = [
    'boris',
    'cindy',
    'kip',
    'core',
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
    'URL': os.getenv('NOFOLLOW_BROKER_URL'),
    'USE_SSL': bool(int(os.getenv('NOFOLLOW_BROKER_USE_SSL', 0)))
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Media files (user generated content)
MEDIA_ROOT = os.getenv('NOFOLLOW_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = os.getenv('NOFOLLOW_MEDIA_URL', '/media/')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = os.getenv('NOFOLLOW_STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('NOFOLLOW_STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', '{} {{infile}} {{outfile}}'.format(os.path.join(BIN_FOLDER, 'sassc'))),
)


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


HTML_SANITIZERS = {
    'default': {
        'tags': {
            'a', 'h1', 'h2', 'h3', 'strong', 'em', 'p', 'ul', 'ol',
            'li', 'br', 'sub', 'sup', 'hr', 'quote', 'blockquote', 'img',
            'code', 'pre'
        },
        'attributes': {
            'a': ('href', 'name', 'target', 'title', 'id', 'rel'),
            'img': ('src', 'alt')
        }
    }
}


# Boris Spider Configuration

BORIS_SPIDERS = {
    'MERCURY_PARSER': {
        'API_KEY': os.getenv('MERCURY_PARSER_API_KEY')
        }
    }


# Logging Configuration
LOG_FILE = os.getenv('NOFOLLOW_SITE_LOG_FILE')
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s:%(module)s %(process)d %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s:%(module)s %(lineno)d %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
            },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': LOG_FILE,
            'maxBytes': 16 * 1024 * 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends:': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
            },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

for app in APPS:
    LOGGING['loggers'][app] = {
        'handlers': ['console', 'file'],
        'level': 'DEBUG' if DEBUG else 'INFO',
        'propagate': False
        }
