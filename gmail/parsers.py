import httplib2

from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from inbox.models import ImportSession, MailContact, MailMessage, MailContactMap
from contact.models import UserContact
from apiclient.discovery import build

from . import Auth
from contact import MailDirection


class InboxImport:
    def __init__(self, user):
        self.user = user
        self.service = Auth.get_gmail_srv(user)
        self.count = 0
        self.max_count = 20
        self.is_refresh = False
        self.can_import = True

    def __process_response(self, response):
        if response['messages']:
            for message in response['messages']:
                print '***MSG ID: %d %s' % (self.count, message['id'])
                mail_import = MailImport(message['id'], self.service, self.user)
                mail_import.import_msg()
                self.count += 1 if mail_import.is_success else 0
                if (self.count > self.max_count) or (self.is_refresh and mail_import.is_duplicate):
                    self.can_import = False
                    break
        return

    def __import(self):
        response = self.service.users().messages().list(userId='me').execute()
        self.__process_response(response)

        while 'nextPageToken' in response and self.can_import:
            # for i in range(1, 1):
            # if response['nextPageToken']:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId='me', pageToken=page_token).execute()
            self.__process_response(response)
        return self.save_session()

    def import_new(self):
        self.is_refresh = True
        return self.__import()

    def import_old(self):
        self.is_refresh = False
        return self.__import()

    def save_session(self):
        im = ImportSession()
        im.count = self.count
        im.user = self.user
        im.save()
        return im


class ContactsImport:
    def __init__(self, response, type, user, mail):
        self.mail = mail
        self.response = response.strip()
        self.type = type
        self.user = user
        ids = self.response.strip().split('>,')
        contacts = [self.__get_contact(m) for m in ids]
        self.contacts = []
        for c in contacts:
            if ',' in c.email:
                self.contacts += [self.__get_contact(m) for m in c.email.split(',')]
            else:
                self.contacts += [c]
        pass

    def __get_contact(self, resp):
        resp = resp.replace(';', '').replace('>', '').replace('"', '').replace("'", "")
        arr = [a.strip() for a in resp.split('<')]
        contact = MailContact(email=arr[-1].lower())
        contact.name = arr[0] if len(arr[0]) > 0 else arr[-1]
        contact.name = contact.name.split('@')[0][0:120]
        return contact

    def __save_contact(self, contact):
        try:
            contact = MailContact.objects.get(email=contact.email, user_contact__user__id=self.user.id)
        except ObjectDoesNotExist:
            user_contact = UserContact()
            user_contact.user = self.user
            user_contact.name = contact.name
            user_contact.category = self.mail.category
            user_contact.save()
            contact.user_contact = user_contact
            contact.save()
        return contact

    def save(self):
        if len(self.contacts) > 4:  #or self.type == MailDirection.CC:
            return
        for c in [c for c in self.contacts if c.email != self.user.email and len(c.email) > 4]:
            c = self.__save_contact(c)
            contact_mail = MailContactMap()
            contact_mail.mail_contact = c
            contact_mail.mail = self.mail
            contact_mail.type = self.type
            contact_mail.save()


class MailImport:
    def __init__(self, msg_id, service, user):
        self.service = service
        self.mail = MailMessage(user=user)
        self.mail.message_id = msg_id
        self.user = user
        self.contact_imports = []
        self.is_duplicate = False
        self.is_success = False
        self.mail_resp = None

    def __is_exist(self):
        try:
            MailMessage.objects.get(message_id=self.mail.message_id)
            return True
        except ObjectDoesNotExist:
            return False

    def __import_contacts(self, response, dir_type):
        contact_in = ContactsImport(response, dir_type, self.user, self.mail)
        if len([c for c in contact_in.contacts if c.email == self.user.email]):
            self.mail.type = dir_type
        self.contact_imports.append(contact_in)

    def __import_msg(self):
        self.mail_resp = self.service.users().messages().get(userId='me', id=self.mail.message_id).execute()
        self.__set_labels()
        self.__import_from_header()

    def __set_labels(self):
        if None != self.mail_resp.get('labelIds'):
            labels = self.mail_resp['labelIds']
            self.mail.folder = labels[0].lower()
            self.mail.category = labels[1].split("_")[-1].lower() if len(labels) > 1 else "personal"

    def __import_from_header(self):
        for head in self.mail_resp['payload']['headers']:
            name = head['name'].lower()
            value = head['value']
            if MailDirection.value(name):
                self.__import_contacts(value, MailDirection.value(name))
            elif name == 'date':
                if len(value) > 28:
                    self.mail.date = datetime.strptime(value[0:25].strip(), "%a, %d %b %Y %X")
                else:
                    self.mail.date = datetime.strptime(value[0:20].strip(), "%d %b %Y %X")
            elif name == 'subject':
                self.mail.subject = value
        #this is handle mails to arun.ghosh@gmail.com
        self.mail.type = self.mail.type if self.mail.type else MailDirection.TO

    def import_msg(self):
        if not self.__is_exist():
            self.__import_msg()
            if self.mail.date:
                self.mail.save()
                # print len(self.contact_imports)
                [c.save() for c in self.contact_imports]
                self.is_success = True
            else:
                # TODO: get contact info from thread
                pass

        else:
            self.is_duplicate = True