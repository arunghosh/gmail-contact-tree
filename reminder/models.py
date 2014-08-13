from django.db import models
from contact.models import UserContact
from inbox.models import MailMessage
from common.models import BaseModel


class Reminder(BaseModel):
    contact = models.ForeignKey(UserContact)
    date = models.DateTimeField()
    remark = models.CharField(max_length=256, blank=True)
    status = models.SmallIntegerField(default=0)
    mail = models.ForeignKey(MailMessage, null=True)



