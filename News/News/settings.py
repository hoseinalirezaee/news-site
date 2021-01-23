import os

from django.utils.translation import gettext_noop

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'ReplaceThisValueWithYourVERStrongSECRetKEy'

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'db.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'db',
    'api',
    'web',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'News.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web.context_processors.get_root_categories'
            ],
        },
    },
]

WSGI_APPLICATION = 'News.wsgi.application'

DATABASES = {
    'default': {
        'NAME': 'news',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('DATABASE_USER', 'username'),
        'PASSWORD': os.environ.get('DATABASE_PASS', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': int(os.environ.get('DATABASE_PORT', '5432')),
        'OPTIONS': {
            'connect_timeout': 10
        }
    }
}


LANGUAGE_CODE = 'en'

LOCALE_PATH = [os.path.join(BASE_DIR, 'web/locale')]

LANGUAGES = [
    ('fa', gettext_noop('Persian')),
    ('en', gettext_noop('English'))
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/statics/'
STATIC_ROOT = 'statics/'
