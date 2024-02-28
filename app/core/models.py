"""
Database models..
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""
    # extra_field is for any keyword arguments
    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user"""
        # this way we can access the model we associated with.
        if not email:
            raise ValueError("The email should be inserted")
        user = self.model(email=self.normalize_email(email), **extra_field)
        # this way we take the password and encrypt it through a hashing
        # mechanism this means it has a one way encryption that can't be
        # reversed
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra):
        """Create, save a super user"""
        super_user = self.create_user(email, password, **extra)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    # Can the user login in the admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # adding this is duplicate as it is already in PermissionsMixin
    # is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
