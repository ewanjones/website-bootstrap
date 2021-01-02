from typing import Iterable

from django.core.mail import EmailMessage

from data.comms import models

from core.utils import logger

class EmailError(Exception):
    pass


class StdoutEmailer:
    """
    An email sender which which prints to stdout but saves an audit model as well.
    """

    @classmethod
    def create_message(cls, *, subject, body, from_email, to: Iterable):
        email = EmailMessage(subject, body, from_email, to)
        return cls(email)

    def __init__(self, email: EmailMessage):
        self._email = email
        self._audit = None

    def send(self):
        self._create_audit()
        
        # Might need to refactor line to make it a bit more easier to read?
        email_template = "========================\nFrom: {0}\nTo: {1}\n------------------------\nSubject: {2}\n{3}\n------------------------\n========================".format(self._email.from_email, self._email.to, self._email.subject, self._email.body)
        
        logger.print(email_template)
        
        self._mark_sent()

    def _create_audit(self):
        self._audit = models.Email.objects.create(
            from_email=self._email.from_email,
            to_email=",".join(self._email.to),
            subject=self._email.subject,
            body=self._email.body,
        )

    def _mark_sent(self):
        if not self._audit:
            raise EmailError("Please create an audit instance before marking sent")
        self._audit.mark_sent()


class TestEmailer:
    """
    An email which uses the django email API for use in tests.

    This allows us to use the django.core.mail to check for email sending.
    """

    @classmethod
    def create_message(cls, *, subject, body, from_email, to: Iterable):
        email = EmailMessage(subject, body, from_email, to)
        return cls(email)

    def __init__(self, email: EmailMessage):
        self._email = email
        self._audit = None

    def send(self):
        self._email.send()
