import os
from .base import *
from .jazzmin import *


env = os.environ.get("ENVIRONMENT", default="local").lower()

try:
    if env == "local":
        from .local import *
    if env == "dev":
        from .dev import *
    if env == "prod":
        from .prod import *
except ImportError as e:
    print(f"No setting found {e}")
