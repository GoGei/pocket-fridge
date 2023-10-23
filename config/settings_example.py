from default_settings import *

SECRET_KEY = 'your-secret-key'

DEBUG = True
TEST_MODE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = True
TEMPLATES[0]['OPTIONS']['debug'] = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'

HOST_PORT = '4482'
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

DATABASES['default']['PASSWORD'] = 'pocket-fridge-password'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''

STRIPE_API_KEY = ''

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
