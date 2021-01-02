from envparse import env

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ["server", "localhost", "178.62.29.196"]

# Emails

EMAIL_SENDER = "core.email.SmtpEmailer"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = TECH_EMAIL  # noqa
EMAIL_HOST_PASSWORD = env.str("TECH_EMAIL_PASSWORD", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True


STATIC_URL = "/static/"
BASE_URL = "http://178.62.29.196"
REACT_BUNDLE_BASE_URL = STATIC_URL + "bundle.js"

TWILIO_SERVICE_NAME = "LOCAL"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
