from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager

from users.category import Category


class UserManager(BaseUserManager):
    def create_user(
        self, username, email, password=None, category: str = "Personal Account"
    ):
        try:
            category_object = Category.objects.get(name__iexact=category)
        except ObjectDoesNotExist:
            category_object, _ = Category.objects.get_or_create(
                name="Personal Account", defaults={"user": "Personal Account"}
            )

        if not username:
            raise ValueError("Please provide a username")

        if not email:
            raise ValueError("Users must have an email address.")

        #
        # check if info already exists
        #
        try:
            self.model.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        else:
            raise ValueError(
                "The username you've provided is in use. Please use a unique username"
            )

        if email:
            try:
                self.model.objects.get(email=email)
            except ObjectDoesNotExist:
                pass
            else:
                raise ValueError(
                    "The email you've provided already exists. Please use a unique email"
                )
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
            category=category_object,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, password, category: str = "Personal Account"
    ):

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
