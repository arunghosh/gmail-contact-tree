from django.db import models
from common.models import BaseModel
from contact.models import UserContact
from auth.models import MyUser


class MobileContact(BaseModel):
    number = models.CharField(max_length=32)
    user_contact = models.ForeignKey(UserContact)
    remark = models.CharField(max_length=64, null=True, blank=True)


class MobileMessage(BaseModel):
    date = models.DateTimeField()
    user = models.ForeignKey(MyUser)
    mobile_contact = models.ForeignKey(MobileContact)


class MobileCall(BaseModel):
    duration = models.IntegerField()
    date = models.DateTimeField()
    mobile_contact = models.ForeignKey(MobileContact)
    user = models.ForeignKey(MyUser)
