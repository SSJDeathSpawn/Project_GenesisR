from django.db import models
from django.contrib.auth.models import AbstractUser

class UserExtended(AbstractUser):
    following = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
