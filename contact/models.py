from django.db import models
from common.models import BaseModel
from auth.models import MyUser
from . import ContactStatus


class UserContact(BaseModel):
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(MyUser)
    status = models.SmallIntegerField(default=ContactStatus.follow)
    category = models.CharField(max_length=64, blank=True)

    @property
    def mails(self):
        mails = [cmm.mail for m_c in self.mailcontact_set.all() for cmm in m_c.mailcontactmap_set.all()]
        mails.sort(key=lambda x: x.date, reverse=True)
        return mails

    @property
    def last_contacted_on(self):
        dates = [m.date for m in self.mails]
        dates.sort()
        return dates[-1].date()

