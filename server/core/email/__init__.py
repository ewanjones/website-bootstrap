from django.conf import settings
from django.utils import module_loading

from .fake import StdoutEmailer, TestEmailer  # noqa
from .smtp import SmtpEmailer  # noqa


def get_client():
    return module_loading.import_string(settings.EMAIL_SENDER)
