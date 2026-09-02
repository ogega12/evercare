"""
Django settings for garage_website (config).

This settings file is configured to be production-ready while still providing
sane defaults for local development. Sensitive values are read from
environment variables. PostgreSQL is supported via DATABASE_URL.
"""

from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Read environment variables
ENV = os.environ
def env_bool(name, default=False):
    return ENV.get(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}

DEBUG = env_bool('DEBUG', True)
SECRET_KEY = ENV.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = get_random_secret_key()
    else:
        raise ImproperlyConfigured('SECRET_KEY must be set when DEBUG=False.')

ALLOWED_HOSTS = [host.strip() for host in ENV.get(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver'
).split(',') if host.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'garage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'garage.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - support DATABASE_URL env var (PostgreSQL) or fallback to sqlite for local
DATABASE_URL = ENV.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    except Exception:
        # If dj_database_url is not installed, fallback to simple parsing
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': ENV.get('POSTGRES_DB', 'garage_db'),
                'USER': ENV.get('POSTGRES_USER', 'postgres'),
                'PASSWORD': ENV.get('POSTGRES_PASSWORD', ''),
                'HOST': ENV.get('POSTGRES_HOST', 'localhost'),
                'PORT': ENV.get('POSTGRES_PORT', '5432'),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = ENV.get('TIME_ZONE', 'Africa/Nairobi')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email - keep console backend as default for development
EMAIL_BACKEND = ENV.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG
    else 'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = ENV.get('EMAIL_HOST', '')
EMAIL_PORT = int(ENV.get('EMAIL_PORT', '587'))
EMAIL_HOST_USER = ENV.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = ENV.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
DEFAULT_FROM_EMAIL = ENV.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'webmaster@localhost')

# Security settings for production
if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', False)
    SECURE_HSTS_SECONDS = int(ENV.get('SECURE_HSTS_SECONDS', '0'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
    SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', False)
    SECURE_REFERRER_POLICY = ENV.get('SECURE_REFERRER_POLICY', 'same-origin')

CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in ENV.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

# Third party / local settings
WHATSAPP_NUMBER = ENV.get('WHATSAPP_NUMBER', '+254723900873')
GOOGLE_MAPS_API_KEY = ENV.get('GOOGLE_MAPS_API_KEY', '')
