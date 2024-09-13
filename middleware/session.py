import uuid

from settings import REDIS


class RedisSessionMiddleware:
    def __init__(self, app):
        self.app = app
        self.redis_client = REDIS

    async def __call__(self, scope, receive, send):
        session_id = None

        # Extract session ID from cookies
        if 'cookie' in scope:
            cookies = dict(cookie.split('=') for cookie in scope['cookie'].split('; '))
            session_id = cookies.get('session_id')

        # Retrieve session data from Redis
        if session_id and await self.redis_client.exists(session_id):
            scope['session'] = await self.redis_client.hgetall(session_id)
        else:
            # Create a new session if no valid session exists
            if not session_id:
                session_id = str(uuid.uuid4())
                scope['headers'].append((b'Set-Cookie', f'session_id={session_id}'.encode()))
            scope['session'] = {}

        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                if scope['session']:
                    await self.redis_client.hmset(session_id, scope['session'])
            await send(message)

        await self.app(scope, receive, send_wrapper)
