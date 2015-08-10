import os
from datetime import timedelta

from celery.schedules import crontab
from getenv import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_ENVIRONMENT_VARIABLES = [
    'CDPT_ENVIRONMENT',
    'CDPT_DJANGO_SECRET_KEY',
    'CDPT_MAILGUN_USER',
    'CDPT_MAILGUN_PASS',
    'CDPT_ADMIN_PASS',
    'CDPT_DJANGO_PAYU_BASE_URL',
    'CDPT_DJANGO_PAYU_POS_ID',
    'CDPT_DJANGO_PAYU_POS_AUTHORIZATION_KEY',
    'CDPT_IFIRMA_USER',
    'CDPT_IFIRMA_INVOICE_KEY',
    'CDPT_IFIRMA_USER_KEY',
    'CDPT_WEB_CLIENT_ADDRESS',
]

MISSING_ENVIRONMENT_VARIABLES = []
for e in REQUIRED_ENVIRONMENT_VARIABLES:
    if not env(e, required=False):
        MISSING_ENVIRONMENT_VARIABLES.append(e)

if MISSING_ENVIRONMENT_VARIABLES:
    raise Exception(
        '\n\nFollowing environment variables are missing:\n\t{}\n\nAdd all missing variables to: {}'.format(
            '\n\t'.join(MISSING_ENVIRONMENT_VARIABLES), '{}'.format(os.path.join(BASE_DIR, 'environment')
                                                                    ))
    )


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('CDPT_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('CDPT_ENVIRONMENT') != 'PRODUCTION'

ALLOWED_HOSTS = [
    'backend.codepot.pl',
    'backend.codepot.pl.'
]

INSTALLED_DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

INSTALLED_THIRD_PARTY_APPS = (
    'django_nose',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_payu',
    'haystack',
)

INSTALLED_HOME_GROWN_APPS = (
    'codepot',
)

INSTALLED_APPS = INSTALLED_DJANGO_APPS + INSTALLED_THIRD_PARTY_APPS + INSTALLED_HOME_GROWN_APPS

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'codepot.middleware.DisableCSRF',
    'django_payu.middleware.DjangoPayExceptionsMiddleware',
)

# Disable https forcing on development environment
SSLIFY_DISABLE = env('CDPT_ENVIRONMENT') != 'PRODUCTION'
protocol = 'https' if env('CDPT_ENVIRONMENT') == 'PRODUCTION' else 'http'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', protocol)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'codepot.middleware.custom_exception_handler',
}

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'), ],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': env('POSTGRES_PORT_5432_TCP_ADDR'),
        'PORT': env('POSTGRES_PORT_5432_TCP_PORT'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = ('token',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nocapture',
    '--nologcapture',
]


# http://www.webforefront.com/django/setupdjangologging.html
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(funcName)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'log', 'codepot.log'),
            'backupCount': 90,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'codepot': {
            'handlers': ['console', 'file', ],
            'level': 'DEBUG',
        },
    },
}

# MailGun
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = env('CDPT_MAILGUN_USER')
EMAIL_HOST_PASSWORD = env('CDPT_MAILGUN_PASS')
EMAIL_PORT = 587

# Celery
BROKER_URL = 'redis://{}:{}'.format(env('REDIS_PORT_6379_TCP_ADDR'), env('REDIS_PORT_6379_TCP_PORT'))
CELERY_IMPORTS = ('celerytq.tasks',)
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'every-5-seconds-check-payu-payment-status': {
        'task': 'celerytq.tasks.check_payu_payment_status',
        'schedule': timedelta(seconds=5),
    },
    'every-15-seconds-send-payment-notification': {
        'task': 'celerytq.tasks.send_payment_notification',
        'schedule': timedelta(seconds=15),
    },
    'every-3-minutes-generate-and-send-invoice': {
        'task': 'celerytq.tasks.generate_and_send_invoice',
        'schedule': crontab(minute='*/3'),
    },
    'every-10-minutes-update-workshops-full-text-search': {
        'task': 'celerytq.tasks.update_workshops_full_text_search',
        'schedule': crontab(minute='*/10'),
    },
}

# Haystack
HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'URL': 'http://{}:{}'.format(env('ELASTICSEARCH_PORT_9200_TCP_ADDR'), env('ELASTICSEARCH_PORT_9200_TCP_PORT')),
    'INDEX_NAME': 'haystack',
  },
}

print(HAYSTACK_CONNECTIONS)

# PayU
DJANGO_PAYU_BASE_URL = env('CDPT_DJANGO_PAYU_BASE_URL')
DJANGO_PAYU_POS_ID = env('CDPT_DJANGO_PAYU_POS_ID')
DJANGO_PAYU_POS_AUTHORIZATION_KEY = env('CDPT_DJANGO_PAYU_POS_AUTHORIZATION_KEY')
DJANGO_PAYU_LOG_FILE = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'log', 'codepot-payu.log'),

# MCE bank account data
MCE_BANK_ACCOUNT = {
    'accountNo': '81109028510000000122488798',
    'street': 'Osowska 23/6',
    'zipCode': '04-302',
    'city': 'Warszawa',
}

MAX_TICKETS = 270

WEB_CLIENT_ADDRESS = env('CDPT_WEB_CLIENT_ADDRESS')

print('Current environment: {}'.format(env('CDPT_ENVIRONMENT')))
print('Base dir: {}'.format(BASE_DIR))
