import datetime


from peewee import DateTimeField, TextField, UUIDField

from advent.Model.basemodel import AdventBaseModel


class FIELDS:
    FROM = 'From'
    RECEIVED = 'Received'
    SEND = 'Sent'
    TO = 'To'

    VALID = [FROM, RECEIVED, SEND, TO]


class SMS(AdventBaseModel):
    """short message service"""
    created_date = DateTimeField(default=datetime.datetime.now)
    send_dt = DateTimeField(null=True)
    received_dt = DateTimeField(null=True)
    msg = TextField()
    msgto = TextField()
    msgfrom = TextField()

    @classmethod
    def create(cls, to: str, msg: str, todb: bool = False):
        sms = cls(msg=msg, msgto=to, msgfrom='me')
        if todb:
            sms.save()
        return sms

    @classmethod
    def fromstring(cls, str: str, todb: bool = True):

        lines = str.splitlines()

        attr = dict(map(lambda s: s.split(": "), (filter(lambda field: ': ' in field, lines))))

        [attr.pop(k) for k in list(attr.keys()) if k not in FIELDS.VALID]

        msg = lines[-1]
        msgfrom = attr.get(FIELDS.FROM, '')
        msgto = attr.get(FIELDS.TO, '')

        sms = cls(msg=msg, msgto=msgto, msgfrom=msgfrom)
        if todb:
            sms.save()
        return sms

    @property
    def length(self):
        return -(-len(self.msg) // 160)

    def checkforkeywords(self, keywords: list) -> bool:
        for word in keywords:
            if word.lower() in self.msg.lower():
                return True
        return False

    def tostring(self):
        return ("To: {0}\n\n{1}").format(self.msgto, self.msg)
