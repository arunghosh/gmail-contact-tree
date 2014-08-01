
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