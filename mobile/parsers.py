import json
from .models import MobileCall, MobileContact
from contact.models import UserContact
from datetime import datetime
from auth.models import MyUser


class ImportMobile:

    def __init__(self, request):
        info = json.loads(request.read())
        print info
        self.call_list = info['data']
        self.user = MyUser.objects.get(phone=info['number'])
        self.user.mobile_updated_on = info['date']
        self.user.save()
        self.__import_contacts()

    # def __update_last_contacted

    def __get_contact(self, contact_info):
        number = contact_info['number'][-10:]
        # code = contact_info['number'][0:-10]
        name = contact_info['name']
        try:
            mobile_contact = MobileContact.objects.get(number=number, user_contact__user__id=self.user.id)
        except:
            mobile_contact = MobileContact()
            mobile_contact.number = number
            mobile_contact.user_contact = self.__create_user_contact(name)
            mobile_contact.save()
        return mobile_contact

    def __create_user_contact(self, name):
        user_contact = UserContact()
        user_contact.name = name
        user_contact.user = self.user
        user_contact.category = "Mobile"
        user_contact.save()
        return user_contact

    def __import_contacts(self):
        for c in self.call_list:
            call = MobileCall()
            call.mobile_contact = self.__get_contact(c)
            call.duration = c['duration']
            call.is_call = c['type'] == 'call'
            call.date = datetime.strptime(c['datetime'], "%d-%m-%Y %X")
            call.save()




