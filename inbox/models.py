from django.db import models
from common.models import BaseModel
from auth.models import MyUser
from contact import ContactStatus
from contact.models import UserContact


class MailContact(BaseModel):
    email = models.EmailField(max_length=128)
    remark = models.CharField(max_length=64, null=True, blank=True)
    user_contact = models.ForeignKey(UserContact)


class MailMessage(BaseModel):
    message_id = models.CharField(max_length=64)
    mail_client = models.CharField(max_length=32, default="gmail")
    date = models.DateTimeField()
    folder = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(MyUser)
    subject = models.CharField(max_length=256)

    class Meta:
        unique_together = ('message_id', 'mail_client', 'user')


class MailContactMap(BaseModel):
    mail_contact = models.ForeignKey(MailContact)
    mail = models.ForeignKey(MailMessage)
    type = models.SmallIntegerField()


class ImportSession(BaseModel):
    user = models.ForeignKey(MyUser)
    count = models.IntegerField()