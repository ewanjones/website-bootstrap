import textwrap
import uuid

from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError
from django.urls import reverse

from core.email import get_client
from data.accounts import models as account_models


class UnableToRegister(Exception):
    pass


@transaction.atomic
def register(*, full_name, nickname, email, phone, password, business_name):
    """
    Create a user and business.
    """

    activation_code = uuid.uuid4().hex

    try:
        user = account_models.User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            nickname=nickname,
            phone=phone,
            activation_code=activation_code,
        )
    except IntegrityError:
        raise UnableToRegister("Couldn't create an account with this email")

    activation_link = settings.BASE_URL + reverse(
        "account-activate", kwargs={"code": activation_code, "user_id": user.id}
    )
    body = textwrap.dedent(
        f"""
        Welcome to Escalo!

        Visit {activation_link} to activate your account
    """
    ).strip()
    email_client = get_client()
    email = email_client.create_message(
        from_email=settings.TECH_EMAIL,
        to=[user.email],
        subject="Welcome to my website",
        body=body,
    )
    email.send()

    return user


def request_reset_password(*, email):
    try:
        user = account_models.User.objects.get(email=email)
    except account_models.User.DoesNotExist:
        # We can't find the email in our system so don't do anything
        return

    reset_code = uuid.uuid4().hex
    user.set_reset_code(reset_code)

    url = settings.BASE_URL + reverse("password-reset", kwargs={"code": reset_code})
    body = textwrap.dedent(
        f"""
        Click the link below to reset your password:
        {url}
    """
    )

    email_client = get_client()
    email = email_client.create_message(
        from_email=settings.TECH_EMAIL,
        to=[email],
        subject="Reset your password",
        body=body,
    )
    email.send()


def reset_password(user, new_password):
    user.set_password(new_password)
    user.set_reset_code("")
