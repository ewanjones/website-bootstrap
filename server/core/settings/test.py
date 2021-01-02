from .base import *  # noqa

DEBUG = True

BUNDLE_BASE_URL = "http://localhost:3000/"
BASE_URL = "testserver"


EMAIL_SENDER = "core.email.TestEmailer"

# Replace the authentication with basic auth for testing to remove the need for providing
# CSRF tokens. We also need to remove it from the middleware.

MIDDLEWARE = [
    item
    for item in MIDDLEWARE  # noqa
    if item != "django.middleware.csrf.CsrfViewMiddleware"
]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [  # noqa
    "rest_framework.authentication.BasicAuthentication"
]
