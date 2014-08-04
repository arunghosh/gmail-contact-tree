import json
from contact.models import UserContact
from .models import Reminder


class ReminderStatus:
    active = 0,
    snooze = 1,
    inactive = 2,
    completed = 3


def add_reminder(request):
    data = json.loads(request.POST)
    cid = data.get('cid')
    date = data.get('date')
