import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://cheerful-regular-goat.ngrok-free.app",
]
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "webdb",
        "USER": "superuser",
        "PASSWORD": "admin_admin",
        "HOST": "db",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://localhost:4566",
#     "https://localhost:4566",
#
# ]


STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)


SYSTEM_USERNAME = "system-user"
