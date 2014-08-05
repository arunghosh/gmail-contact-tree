
class ContactStatus:
    follow = 0
    not_follow = 1
    merged = 2
    removed = 3

    @classmethod
    def get_active(cls, user):
        return user.usercontact_set.filter(status__lte=ContactStatus.not_follow)


class MailDirection:
    TO = 1
    FROM = 2
    CC = 3

    _look_up = {"from": FROM,
                "to": TO,
                "cc": CC }

    @classmethod
    def value(cls, direction):
        return cls._look_up.get(direction, None)


class CommStat:

    def __init__(self, month, mail_count, call_count, index):
        self.month = month
        self.mail_count = mail_count
        self.call_count = call_count
        self.index = index


class CommItem:
    mail = 1
    message = 2
    call = 3

    def __init__(self, date, c_type, remark, direction, mail_id=None):
        self.date = date
        self.remark = remark
        self.type = c_type
        self.mail_id = mail_id
        self.direction = direction

    @classmethod
    def from_mail(cls, m):
        c_type = CommItem.mail if m.type == MailDirection.FROM else cls.mail
        return CommItem(c_type=cls.mail,
                        date=m.date,
                        direction=0 if m.type == MailDirection.FROM else 1,
                        remark=m.subject,
                        mail_id=m.message_id)

    @classmethod
    def from_call(cls, c):
        return CommItem(c_type=cls.call if c.is_call else cls.message,
                        date=c.date,
                        direction=1,
                        remark="")
