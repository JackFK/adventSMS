import datetime

from peewee import TextField, DateTimeField, BooleanField, IntegerField

from advent.Model.basemodel import AdventBaseModel


class Thought(AdventBaseModel):
    """???"""
    msg = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=False)
    day = IntegerField(default=0)
    month = IntegerField(default=0)

    @classmethod
    def create(cls, msg: str, day: int, month: str):
        t = cls(msg=msg, day=day, month=month)
        t.save()
        return t

    @property
    def length(self):
        return 0

    @classmethod
    def oftheday(cls, day: int, month: int):
        return cls.get(cls.day == day, cls.month == month, cls.is_published == False, )

    @classmethod
    def count(cls)->int:
        return cls.select().count()