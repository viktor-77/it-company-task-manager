import os

from dotenv import load_dotenv

from .base import *

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

if RENDER_EXTERNAL_HOSTNAME := os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
	ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('POSTGRES_DB'),
		'USER': os.environ.get('POSTGRES_USER'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
		'HOST': os.environ.get('POSTGRES_HOST'),
		'PORT': int(os.environ.get('POSTGRES_DB_PORT', 5432)),
		'OPTIONS': {
			'sslmode': 'require',
		},
	}
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
