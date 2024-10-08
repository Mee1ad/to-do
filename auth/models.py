from datetime import datetime

from peewee import CharField, ForeignKeyField, DateTimeField

from settings import BaseModel


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True, null=True)
    created_at = DateTimeField(default=datetime.now)


class Login(BaseModel):
    user = ForeignKeyField(User, backref='logins', on_delete='CASCADE', on_update='CASCADE')
    provider = CharField()  # e.g., 'google', 'apple'
    connection_id = CharField()
    idp_id = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            (('user', 'provider'), True),
        )
