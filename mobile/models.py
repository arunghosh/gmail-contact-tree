from django.db import models
from common.models import BaseModel
from contact.models import UserContact
from auth.models import MyUser


class MobileContact(BaseModel):
    number = models.CharField(max_length=32)
    user_contact = models.ForeignKey(UserContact)
    remark = models.CharField(max_length=64, null=True, blank=True)


class MobileCall(BaseModel):
    is_call = models.BooleanField()
    duration = models.IntegerField()
    date = models.DateTimeField()
    mobile_contact = models.ForeignKey(MobileContact)
