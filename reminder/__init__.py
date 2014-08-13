import json
from contact.models import UserContact
from .models import Reminder
from .serializers import ReminderSerializer
from contact.models import UserContact

class ReminderStatus:
    active = 0
    snooze = 1
    inactive = 2
    completed = 3


def add_reminder(request):
    data = json.loads(request.POST)
    cid = data.get('cid')
    date = data.get('date')

def get_active_reminders(cid):
    contact = UserContact.objects.get(pk=cid)
    reminders = list(contact.reminder_set.filter(status=ReminderStatus.active))
    reminders.sort(key=lambda x: x.date)
    slz = ReminderSerializer(reminders, many=True)
    return slz.data