import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://9add-2400-1a00-b012-cb8f-aef3-63b6-1338-6799.ngrok-free.app"
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


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://localhost:4566",
#     "https://localhost:4566",
#
# ]


STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)


SYSTEM_USERNAME = "system-user"
