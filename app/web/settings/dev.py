import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = BASE_DIR

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


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
