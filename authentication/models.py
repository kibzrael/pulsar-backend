from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

import jwt

from authentication.user_manager import UserManager
from media.models import Photo
from users.category import Category


class User(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    # remove null = true
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categoryid", null=False
    )
    solo = models.BooleanField(default=True)
    fullname = models.CharField(max_length=24)
    email = models.EmailField(null=False, max_length=254, verbose_name="Email Address")
    # phone = PhoneNumberField( null=True, max_length=50, verbose_name='Phone Number')
    profile_pic = models.OneToOneField(
        Photo, on_delete=models.SET_NULL, null=True, blank=True
    )
    bio = models.CharField(max_length=80, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(default=timezone.localdate)
    portfolio = models.URLField(null=True, blank=True)

    objects = UserManager()

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username

    def generate_token(self):
        jwt_token = jwt.encode(
            payload={"id": self.id, "username": self.username}, key="rs-pulsar"
        )
        return str(jwt_token)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Provider(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=12, null=False)
    provider_id = models.CharField(max_length=255, null=False)
    access_token = models.CharField(max_length=2048, null=False)
    refresh_token = models.CharField(max_length=255, null=True)
