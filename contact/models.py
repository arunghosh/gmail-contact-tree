from django.db import models
from django.db.models import Q
from common.models import BaseModel
from auth.models import MyUser
from . import ContactStatus, MailDirection
from datetime import datetime, timedelta
from contact import CommItem

class UserContact(BaseModel):
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(MyUser)
    status = models.SmallIntegerField(default=ContactStatus.follow)
    category = models.CharField(max_length=64, blank=True)
    # is_deleted = models.BooleanField(default=False)
    # is_important = models.BooleanField(default=False)
    # is_follow = models.BooleanField(default=True)


    @property
    def mails(self):
        mails = [cmm.mail for m_c in self.mailcontact_set.all() for cmm in m_c.mailcontactmap_set.all()]
        mails.sort(key=lambda x: x.date, reverse=True)
        return mails

    # @property
    # def valid_mails(self):
    #     mails = [cmm.mail for m_c in self.mailcontact_set.all() for cmm in m_c.mailcontactmap_set.all() if
    #              (cmm.mail.type == MailDirection.TO and cmm.type == MailDirection.FROM) or (cmm.mail.type == MailDirection.FROM and cmm.type == MailDirection.TO)]
    #     mails.sort(key=lambda x: x.date, reverse=True)
    #     return self.mails

    @property
    def calls(self):
        calls = [cmm for m_c in self.mobilecontact_set.all() for cmm in m_c.mobilecall_set.all()]
        calls.sort(key=lambda x: x.date, reverse=True)
        return calls

    @property
    def all_communications(self):
        calls = [CommItem.from_call(c) for c in self.calls]
        mails = [CommItem.from_mail(c) for c in self.mails]
        all_comm = mails + calls
        all_comm.sort(key=lambda x: x.date, reverse=True)
        return all_comm

    @property
    def last_contacted_on(self):
        dates_mail = [m.date for m in self.mails if m.type != MailDirection.CC]
        dates_call = [m.date for m in self.calls]
        dates = dates_call + dates_mail
        if len(dates) == 0:
            return (datetime.now() - timedelta(days=360)).date()
        return dates[0].date()

