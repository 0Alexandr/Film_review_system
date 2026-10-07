"""WSGI config for the film review web project."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmreviews.settings")

application = get_wsgi_application()
