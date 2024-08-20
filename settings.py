from peewee import SqliteDatabase, Model
from pydantic_settings import BaseSettings

DB = SqliteDatabase('./db/to-do.sqlite3', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = DB


class Env(BaseSettings):
    domain: str
    workos_api_key: str
    workos_client_id: str

    class Config:
        env_file = '.env'


env = Env()
