#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
    if ENVIRONMENT == "local":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        raise
    execute_from_command_line(sys.argv)
