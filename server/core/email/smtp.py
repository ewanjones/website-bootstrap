from typing import Iterable

from django.core.mail import EmailMessage

from data.comms import models


class EmailError(Exception):
    pass


class SmtpEmailer:
    @classmethod
    def create_message(cls, *, subject, body, from_email, to: Iterable):
        email = EmailMessage(subject, body, from_email, to)
        return cls(email)

    def __init__(self, email: EmailMessage):
        self._email = email
        self._audit = None

    def send(self):
        self._create_audit()
        self._email.send()
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
