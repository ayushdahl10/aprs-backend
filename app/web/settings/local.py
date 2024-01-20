import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://cheerful-regular-goat.ngrok-free.app",
    "http://api.aprstechnologies.com",
]
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "aprsdb",
        "USER": "superuser",
        "PASSWORD": "admin_admin",
        "HOST": "db",
        "PORT": "5432",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://redis:6379"],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://localhost:4566",
#     "https://localhost:4566",
#
# ]


STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)
CELERY_BROKER_REDIS_URL = "redis://localhost:6380"

SYSTEM_USERNAME = "system-user"
