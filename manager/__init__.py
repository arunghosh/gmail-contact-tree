from datetime import datetime, timedelta
from contact import ContactStatus

class ByZoneMgr:

    def __init__(self, user):
        self.contacts = ContactStatus.get_active(user)
        self.safe = 0
        self.inter = 1
        self.unsafe = 2
        self.safe_delta = user.delta_safe
        self.unsafe_delta = user.delta_danger
        self.today = datetime.now().date()

    def __set_zone(self, c):
        delta = (self.today - c.last_contacted_on).days
        c.delta = delta
        if delta < self.safe_delta:
            c.zone = self.safe
        elif delta < self.unsafe_delta:
            c.zone = self.inter
        else:
            c.zone = self.unsafe


    def update_zone(self):
        [self.__set_zone(c) for c in self.contacts]
        return self.contacts


