from peewee import SqliteDatabase, Model

db = SqliteDatabase('advent.db')


class AdventBaseModel(Model):
    class Meta:
        database = db
