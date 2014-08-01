from contact.models import  UserContact
from contact import ContactStatus

class Merge:

    def __init__(self, org_id, dupe_id):
        self.org = UserContact.objects.get(pk=org_id)
        self.dupe = UserContact.objects.get(pk=dupe_id)

    def execute(self):
        self.__merge_mail_contacts()
        self.__merge_mobile_contacts()
        self.dupe.status = ContactStatus.merged
        self.dupe.save()

    def __merge_mobile_contacts(self):
        contacts = self.dupe.mobilecontact_set.all()
        map(self.__merge_contact, contacts)

    def __merge_contact(self, c):
        c.user_contact = self.org
        c.save()

    def __merge_mail_contacts(self):
        contacts = self.dupe.mailcontact_set.all()
        map(self.__merge_contact, contacts)
