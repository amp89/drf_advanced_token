from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAPIKeyLock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="If this object exists, it does not allow this user to change key via the API.", unique=True)
