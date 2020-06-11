import os

from django.utils.translation import gettext_noop

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'hdzfox_u1#jsd^w%&aj!8)j2o$3mh-zz48v9v=i6e#r-lh+%sh'

DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'db.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'NAME': 'django_postgres',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'root',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': 12000
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


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

STATIC_URL = '/static/'
STATIC_ROOT = 'statics/'

MEDIA_ROOT = '/home/hosein/Documents/NewsSite/News/web/static/'
MEDIA_URL = 'http://localhost:8000/static/'
