import datetime

from django.db import models


class Email(models.Model):
    """
    A record of an email to be queued and sent.
    """

    from_email = models.CharField(max_length=100)

    # Postgres is required to store ArrayFields and it isn't feasible to host a DB yet, so we'll
    # just store this in a CharField for now, and split by commas
    to_email = models.CharField(max_length=255)

    subject = models.CharField(max_length=255)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True)

    def mark_sent(self, as_at=None):
        if as_at is None:
            as_at = datetime.datetime.now()
        self.send_at = as_at
        self.save()
