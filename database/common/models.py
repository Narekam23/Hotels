from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('people.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class History(ModelBase):
    numbers = pw.TextField()
    message = pw.TextField()
