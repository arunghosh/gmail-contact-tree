from datetime import datetime, timedelta


class ByZoneMgr:

    def __init__(self, user):
        self.contacts = user.usercontact_set.all()
        self.safe = 0
        self.inter = 1
        self.unsafe = 2
        today = datetime.now()
        self.safe_date = (today - timedelta(days=21)).date()
        self.unsafe_date = (today - timedelta(days=42)).date()

    def __set_zone(self, c):
        if self.safe_date <= c.last_contacted_on:
            c.zone = self.safe
        elif self.unsafe_date >= c.last_contacted_on:
            c.zone = self.unsafe
        else:
            c.zone = self.inter

    def update_zone(self):
        [self.__set_zone(c) for c in self.contacts]
        return self.contacts


