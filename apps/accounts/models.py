from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)   # Email Verification

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name"
    ]

    def __str__(self):
        return self.email