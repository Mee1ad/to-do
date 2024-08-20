import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    created_at: datetime.datetime


class LoginSchema(BaseModel):
    user: UserSchema
    provider: str
    connection_id: str
    idp_id: str
    created_at: datetime.datetime
