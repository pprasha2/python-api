from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def CreateUser(self, email, password=None, **extraFields):
        """Create a new user"""
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(email=self.normalize_email(email), **extraFields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def CreateSuperUser(self, email, password):
        """creates a new super user"""
        user = self.CreateUser(email, password)
        user.IsStaff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """create user model that support email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    IsActive = models.BooleanField(default=True)
    IsStaff = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
