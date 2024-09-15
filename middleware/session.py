import logging
import uuid

from fasthtml.core import MiddlewareBase
from redis.exceptions import DataError
from starlette.datastructures import MutableHeaders

from auth.models import User, Login
from auth.schemas import UserSchema
from common.helper import get_cookies
from settings import REDIS, env
from peewee import DoesNotExist


def build_set_cookie_header(session_id):
    header_value = (
        f"session_id={session_id}; path=/; Max-Age={RedisSessionMiddleware.TWO_WEEKS_IN_SECONDS}; "
        "HttpOnly; SameSite=Lax"
    )
    if env.stage.lower() == 'prod':
        header_value += "; Secure"
    return header_value


def create_guest_user():
    user: UserSchema = User.create(name='Guest')
    Login.create(user_id=user.id, provider='session', connection_id=uuid.uuid4().hex)
    return user


class RedisSessionMiddleware(MiddlewareBase):
    TWO_WEEKS_IN_SECONDS = 1209600  # 14 days

    def __init__(self, app):
        self.app = app
        self.redis_client = REDIS

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            cookies = get_cookies(scope)
            session_id = cookies.get('session_id', None)
            redis_session_byte_dict = {}

            if session_id:
                try:
                    redis_session_byte_dict = await self.redis_client.hgetall(session_id)
                except DataError as e:
                    logging.error(f"Redis DataError: {str(e)}")

            scope['redis_session'] = {
                key.decode('utf-8'): value.decode('utf-8')
                for key, value in redis_session_byte_dict.items()
            }

            if not scope['redis_session']:
                if not session_id:
                    session_id = str(uuid.uuid4())
                scope['redis_session'] = {'session_id': session_id}

            if 'user_id' not in scope['redis_session']:
                user: UserSchema = create_guest_user()
                scope['redis_session']['user_id'] = user.id
            try:
                scope['user'] = User.get(id=scope['redis_session']['user_id'])
            except DoesNotExist:  # means session is expired
                user: UserSchema = create_guest_user()
                scope['redis_session'] = {'session_id': session_id, 'user_id': user.id}
                scope['user'] = user

        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                await self.redis_client.hset(session_id, mapping=scope['redis_session'])

                await self.redis_client.expire(session_id, self.TWO_WEEKS_IN_SECONDS)

                cookie_session_id = cookies.get('session_id', None)
                if not cookie_session_id:
                    headers = MutableHeaders(scope=message)
                    header_value = build_set_cookie_header(session_id)
                    headers.append("Set-Cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)
