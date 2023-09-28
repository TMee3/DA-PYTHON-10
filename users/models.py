from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)









