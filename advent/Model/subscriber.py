import datetime

from peewee import DateTimeField, TextField, BooleanField

from advent.Model.basemodel import AdventBaseModel


class Subscriber(AdventBaseModel):
    """sub"""
    created_date = DateTimeField(default=datetime.datetime.now)
    msg = TextField()
    number = TextField()
    active = BooleanField(default=True)
    unsubscribed_dt = DateTimeField(null=True)
    unsubscribed_msg = TextField(null=True)


    @classmethod
    def subscribe(cls, number: str, msg: str):
        sq = Subscriber.select().where(Subscriber.active == True)
        if sq.where(Subscriber.number == number).exists():
            return None

        sub = cls(msg=msg, number=number)
        sub.save()
        return sub

    def unsubscribe(self, number: str, msg: str):
        self.active = False
        self.unsubscribed_dt = str(datetime.datetime.now)
        self.unsubscribed_msg = msg
        self.save()
        return 0

    @classmethod
    def getallnumbers(cls)->list:
        allsubs = Subscriber.select(Subscriber.number).where(Subscriber.active == True)
        return list(map(lambda x: x.number, allsubs))

    @classmethod
    def count(cls)->int:
        return cls.select().count()
