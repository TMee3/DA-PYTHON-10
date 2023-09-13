from django.db import models
from django.contrib.auth.models import User

class Consent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_given = models.DateTimeField(auto_now_add=True)

