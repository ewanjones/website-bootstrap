from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, *, email, password, nickname, activation_code, phone=None):
        user = self.create(
            email=email,
            nickname=nickname,
            phone=phone,
            activation_code=activation_code,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    nickname = models.CharField(max_length=50)

    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=15, blank=True)

    # Indicates whether the use has activated their account by confirming the email address.
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=255, blank=True)

    password_reset_code = models.CharField(max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def set_active(self):
        self.is_active = True
        self.save()

    def set_reset_code(self, code):
        self.password_reset_code = code
        self.save()
