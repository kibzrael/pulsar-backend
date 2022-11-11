from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

import jwt


from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager
from media.models import Photo

from users.models import Category


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, category: str = "Personal Account"):
        try:
            category_object = Category.objects.get(name__iexact=category)
        except ObjectDoesNotExist:
            category_object = Category.objects.get(name="Personal Account")

        if not username:
            raise ValueError('Please provide a username')

        if not password:
            raise ValueError('Please provide a password')

        if not email:
            raise ValueError('Users must have an email address.')

        #
        # check if info already exists
        #
        try:
            self.model.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        else:
            raise ValueError(
                'The username you\'ve provided is in use. Please use a unique username')

        if email:
            try:
                self.model.objects.get(email=email)
            except ObjectDoesNotExist:
                pass
            else:
                raise ValueError(
                    'The email you\'ve provided already exists. Please use a unique email')
        # if phone:
        #     try:
        #         self.model.objects.get(phone=phone)
        #     except ObjectDoesNotExist:
        #         pass
        #     else:
        #         raise ValueError('The phone number you\'ve provided already exists. Please use a unique phone number')

        user = self.model(
            username=username,
            fullname=username,
            email=self.normalize_email(email),
            category=category_object
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, category: str = "Personal Account"):

        user = self.create_user(
            username,
            category=category,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    # remove null = true
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,  related_name='categoryid', null=False)
    solo = models.BooleanField(default=True)
    fullname = models.CharField(max_length=24)
    email = models.EmailField(
        null=True, max_length=254, verbose_name='Email Address')
    # phone = PhoneNumberField( null=True, max_length=50, verbose_name='Phone Number')
    profile_pic = models.OneToOneField(
        Photo, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.CharField(max_length=80, null=True, blank = True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(default=timezone.localdate)
    portfolio = models.URLField(null=True, blank= True)

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
            payload={'id': self.id, 'username': self.username}, key='rs-pulsar')
        return str(jwt_token)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []





