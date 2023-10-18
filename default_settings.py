"""
Django settings for pocket-fridge project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from mongoengine import register_connection
from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__))) + '/'

SECRET_KEY = None

DEBUG = False
TEST_MODE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = True

ALLOWED_HOSTS = ['*']

SITE_URL = 'pocket-fridge.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = None
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_hosts',
    'django_filters',
    'widget_tweaks',
    'django_tables2',
    'corsheaders',
    'rest_framework',
    'drf_yasg2',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'core.Utils',
    'core.User',
    'core.Licence',
    'core.Fridge',
    'core.ShoppingList',
    'core.Currency',
    'core.Finances',
    'core.Notifications',
    'core.Tasks',
]

AUTH_USER_MODEL = 'User.User'

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_DOMAIN = '.pocket-fridge.local'
SESSION_COOKIE_DOMAIN = '.pocket-fridge.local'

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_HOSTCONF = 'hosts'
DEFAULT_HOST = 'public'
ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'core/templates/',
            BASE_DIR + 'Api/templates/',
            BASE_DIR + 'Manager/templates/',
            BASE_DIR + 'Public/templates/',
            BASE_DIR + 'My/templates/',
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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pocket_fridge',
        'USER': 'pocket_fridge',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

LANGUAGE_CODE = 'en'
LANGUAGE_FALLBACK_CODE = 'en-es'

LANGUAGES = (
    ('en', _('English')),
    # ('ru', _('Russian')),
    ('uk', _('Ukrainian')),
)
LOCALE_PATHS = (
    # os.path.join(BASE_DIR, 'locale'),

    os.path.join(BASE_DIR, 'Api/locale'),
    os.path.join(BASE_DIR, 'Manager/locale'),
    os.path.join(BASE_DIR, 'core/locale'),
    os.path.join(BASE_DIR, 'My/locale'),
    os.path.join(BASE_DIR, 'Public/locale'),
)
DEFAULT_LANGUAGE = 'en'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR + 'static/'
MEDIA_ROOT = BASE_DIR + 'media/'
STATICFILES_DIRS = [
    BASE_DIR + 'htdocs/'
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# folders
USER_PHOTO = 'user_photo'
CONTACT_ICONS_FOLDER = 'contact_icons'
PRIVACY_POLICY_FILEPATH = 'privacy_policy'
TERMS_OF_USE_FILEPATH = 'terms_of_use'
FRIDGE_PRODUCTS_FILEPATH = 'fridge_products'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'COERCE_DECIMAL_TO_STRING': False,
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24  # 24h

CKEDITOR_UPLOAD_PATH = BASE_DIR + 'media/ckeditoruploads/'
CKEDITOR_CONFIGS = {
    'default': {
        "removePlugins": "stylesheetparser",
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Outdent', 'Indent',
             '-', 'Link', 'Unlink',
             'Format',
             '-',
             'Image',
             ],
            ['HorizontalRule',
             '-', 'BulletedList', 'NumberedList',
             '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
             '-', 'SpecialChar',
             '-', 'Source',
             ],
            ['Maximize']
        ],
        'toolbarCanCollapse': True,
        'width': '100%',
        "allowedContent": True,

    },
    'full': {
        'toolbar': 'full',
    },
    'user_feedback_reply': {
        "removePlugins": "stylesheetparser",
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             ],
            ['HorizontalRule',
             '-', 'BulletedList', 'NumberedList',
             '-', 'Cut', 'Copy', 'Paste', 'PasteText',
             ],
            ['Maximize']
        ],
        'toolbarCanCollapse': True,
        'width': '100%',
        "allowedContent": True,
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

ITEMS_PER_PAGE = 20

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

DEFAULT_CURRENCY_CODE = 'UAH'
DEFAULT_CURRENCY_NAME = 'Hryvnia'
DEFAULT_CURRENCY_NUMBER = '980'

DEFAULT_FROM_EMAIL = None
EMAIL_BASE_SITE = "%s://%s.%s" % (SITE_SCHEME, DEFAULT_HOST, SITE_URL)

CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = 'rpc'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_RESULT_EXPIRES = 60

CELERY_QUEUES = {
    'celery': {'exchange': 'celery',
               'exchange_type': 'direct',
               'durable': True},
}

register_connection(alias='notification',
                    host='mongodb://127.0.0.1:27017/pocketfridge_notification',
                    w=0)

USER_GUIDE_URL = 'https://example.com/'
LICENCES_URL = 'https://example.com/'
REPORT_ERROR_URL = 'https://example.com/'
