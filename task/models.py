from peewee import AutoField, CharField, BooleanField

from settings import BaseModel


class Task(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    checked = BooleanField(default=False)
