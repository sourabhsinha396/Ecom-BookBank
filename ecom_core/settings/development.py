import os
import json
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(BASE_DIR, 'secrets/secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    '''Get secret setting or fail with ImproperlyConfigured'''
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "y2=y^&8!8)%#31qc0n-%pq-#xc(xe8az*kx7)h!7ejhtjp)69*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',

 #custom APPs
 'general_pages',
 'user_auth',
 'products',
 'carts',
 'orders',
 'billings',
 'analytics',
 'marketting',

 #Third party Development Only
 'debug_toolbar',
 'rest_framework',
 'taggit', #django taggit

]

MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
 #Debug Toolbar Middle MIDDLEWARE
 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'ecom_core.urls'

TEMPLATES = [
 {
     'BACKEND': 'django.template.backends.django.DjangoTemplates',
     'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'ecom_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.sqlite3',
     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
 }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
 # {
 #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
 # },
 {
     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
 },
 # {
 #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
 # },
 # {
 #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
 # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

##------------########----------######################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dir"),
]
STATIC_ROOT = os.path.join(BASE_DIR,'static_root')
# Static root actually serves the file,
# No need to make static_root manually
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media_root')



# Messages Framework
MESSAGE_TAGS = {
     messages.DEBUG: 'alert-secondary',
     messages.INFO: 'alert-info',
     messages.SUCCESS: 'alert-success',
     messages.WARNING: 'alert-warning',
     messages.ERROR: 'alert-danger',
}

# Debug DebugToolbar
INTERNAL_IPS = ['127.0.0.1']


# Django Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# HTTP
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False

LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'user_auth.User'

# Mailchimp Configrations
MAILCHIMP_API_KEY = get_secret('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = "us10"
MAILCHIMP_EMAIL_AUDIENCE_ID = get_secret('MAILCHIMP_EMAIL_AUDIENCE_ID')
