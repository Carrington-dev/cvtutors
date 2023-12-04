import os
from pathlib import Path
from django.contrib import  messages

BASE_DIR = Path(__file__).resolve().parent.parent
from decouple import config


SECRET_KEY = 'django-insecure-xzaq9p^t-3r7i%8^0*o__ieq3734&&&kt6t=@s)2&ob-3%__^='

DEBUG = True

ALLOWED_HOSTS = ['*', "flexytuta.com"]



INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "whitenoise.runserver_nostatic",

    'django.contrib.sites',
    'django.contrib.sitemaps',

    # 'admin_honeypot',
    'rest_framework',
    'my_auth',
    'panel',
    'tutor',
    'contact',
    'cart',
    'pay',
    'learn',
    'crispy_forms',
    'embed_video',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flexyweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.show_me',
                'learn.context_processors.all_modules',
                'my_auth.context_processors.show_countries',
            ],
        },
    },
]

WSGI_APPLICATION = 'flexyweb.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'my_auth.NewUser'

#Default Paths Of The Apps
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
# STATIC_ROOT = os.path.join(BASE_DIR, "static_files/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATIC_ROOT = os.path.join(BASE_DIR, "static_files/")

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MESSAGE_TAGS = {
    messages.DEBUG : 'alert-info',
    messages.INFO : 'alert-info',
    messages.SUCCESS : 'alert-success',
    messages.WARNING : 'alert-warning',
    messages.ERROR : 'alert-danger',
    # messages.ERROR: 'danger',
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'

# AWS_ACCESS_KEY_ID = 'AKIA2YXVXV2SZ3WLDL7M'
# AWS_SECRET_ACCESS_KEY = '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'

# Account ID: 7403-2347-1013
# IAM user: mytuta

# AUTHENTICATION_BACKENDS = ['my_auths.backends.EmailBackend']


CRISPY_TEMPLATE_PACK = 'bootstrap4'
GRAPPELLI_ADMIN_TITLE = "Stemgon Softwares"
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_SSL = config('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL = 'FlexyTuta <admin@mytuta.co.za>'


# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'server145.web-hosting.com'
# EMAIL_HOST_USER = 'admin@stemgon.co.za'
# EMAIL_HOST_PASSWORD = '#Mulalo96'
# DEFAULT_FROM_EMAIL = 'FlexyTuta Team <admin@stemgon.co.za>'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
LOG_FILE = os.path.join(BASE_DIR, 'logs/stderr.log')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'oftmart', 
#         'USER': 'root', 
#         'PASSWORD': '#Mulalo96',
#         'HOST': '127.0.0.1', 
#         'PORT': '5432',
#     }
# }


DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 1
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
SITE_ID = 1

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'
CSRF_TRUSTED_ORIGINS = [ 'https://b145-196-21-43-5.ngrok-free.app', "https://www.b145-196-21-43-5.ngrok-free.app"]
