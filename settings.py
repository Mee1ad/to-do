import redis.asyncio as redis
from peewee import SqliteDatabase, PostgresqlDatabase, Model
from pydantic_settings import BaseSettings


class Env(BaseSettings):
    stage: str
    domain: str
    workos_api_key: str
    workos_client_id: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = '.env'
        extra = "ignore"


env = Env()

if env.stage.lower() == 'prod':
    DB = PostgresqlDatabase(
        env.postgres_db,
        user=env.postgres_user,
        password=env.postgres_password,
        host='db',
        port=5432
    )
    REDIS = redis.from_url("redis://redis:6379/0")


else:
    DB = SqliteDatabase('./db/to-do.sqlite3', pragmas={'foreign_keys': 1})
    REDIS = redis.from_url("redis://localhost:6379/0")


class BaseModel(Model):
    class Meta:
        database = DB
