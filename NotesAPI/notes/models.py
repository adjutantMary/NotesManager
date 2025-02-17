from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.db import models


# The `UserManager` class provides methods to create regular users and superusers with specified
# attributes.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Users must have an username")
        if email is None:
            raise TypeError("Users must have an email")

        user = self.model(username=username, email=self.normalize_email(email=email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password")

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


# The `User` class defines a custom user model in Django with fields for username, email, activation
# status, staff status, timestamps, and a method to generate a JWT token.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=128, null=False, unique=True)
    email = models.EmailField(db_index=True, max_length=256, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.timestamp())},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token.decode("utf-8")


# The `Note` class defines a model with fields for user, title, content, creation date, and last
# update date in a Django application.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
