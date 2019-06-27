from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserExtendedManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('PROVIDE A PROPER EMAIL!')
        if not username:
            raise ValueError('PROVIDE A USERNAME!')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(username, email, password, **extra_fields)

class UserExtendedR(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=25, unique=True)
    aboutme = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserExtendedManager()

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.username

    def get_long_name(self):
        return self.username