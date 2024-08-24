from peewee import PostgresqlDatabase, Model
from pydantic_settings import BaseSettings

DB = PostgresqlDatabase(
    'verceldb',  # Replace with your database name
    user='default',  # Replace with your username
    password='ZoR0kaFWbO8y',  # Replace with your password
    host='ep-wild-sun-a2bs3soo-pooler.eu-central-1.aws.neon.tech',  # Replace with your host if it's different
    port=5432  # Replace with your port if it's different
)


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
