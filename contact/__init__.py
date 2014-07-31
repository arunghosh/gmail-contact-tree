
class ContactStatus:
    follow = 0
    not_follow = 1


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