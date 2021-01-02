from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["server", "localhost"]

# Emails

EMAIL_SENDER = "core.email.StdoutEmailer"

# Urls

BASE_URL = "http://localhost"
BUNDLE_BASE_URL = "http://localhost:3000/"

# Logging configuration for various Streams e.g StdOut, File, Etc

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
