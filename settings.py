from peewee import SqliteDatabase

DB = SqliteDatabase('./db/to-do.sqlite3')

from pydantic_settings import BaseSettings


class Env(BaseSettings):
    domain: str
    workos_api_key: str
    workos_client_id: str

    class Config:
        env_file = '.env'


env = Env()

print(env.model_dump())