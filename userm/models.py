from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("WHO'LL ENTER THE EMAIL?! HUH?!")
        if not username:
            raise ValueError("BUDDY, I WOULD LIKE FOR YOU TO HAVE A NAME!")
        if not password:
            raise ValueError("YOUR ACCOUNT IS NOT SAFE WITHOUT A PASSWORD, YOU KNOW?")

        user =self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user

class UserExtended(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    aboutme = models.CharField(max_length=200)
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["username" "email"]

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.username

    def get_long_name(self):
        return self.username