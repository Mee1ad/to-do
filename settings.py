from peewee import SqliteDatabase
from pydantic_settings import BaseSettings

DB = SqliteDatabase('./db/to-do.sqlite3')


class Env(BaseSettings):
    domain: str
    workos_api_key: str
    workos_client_id: str

    class Config:
        env_file = '.env'


env = Env()
