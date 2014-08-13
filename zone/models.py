from django.db import models
from auth.models import MyUser

class RemovedCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(MyUser)
