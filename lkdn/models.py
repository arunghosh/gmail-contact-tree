from django.db import models
from auth.models import MyUser

# Create your models here.


class LnContact(models.Model):
    name = models.CharField(max_length=64)
    headline = models.CharField(max_length=128, blank=True)
    image_url = models.URLField(blank=True)
    profile_url = models.URLField(blank=True)
    ln_id = models.CharField(max_length=64)
    user = models.ForeignKey(MyUser)

    class Meta:
        unique_together = ('ln_id', 'user')