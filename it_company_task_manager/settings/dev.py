from .base import *

# Insecure key!
SECRET_KEY = "MS2voxhAzoXEaFrn0D44VrOqpZQnI0n7"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Database
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": BASE_DIR / "db.sqlite3",
	}
}
