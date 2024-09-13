import uuid

import redis.asyncio as redis


class RedisSessionMiddleware:
    def __init__(self, app):
        self.app = app
        self.redis_client = redis.from_url("redis://redis:6379/0")

    async def __call__(self, scope, receive, send):
        # Initialize session_id variable
        session_id = None

        # Extract session ID from cookies
        if 'cookie' in scope:
            cookies = dict(cookie.split('=') for cookie in scope['cookie'].split('; '))
            session_id = cookies.get('session_id')

        # Retrieve session data from Redis
        if session_id:
            scope['session'] = await self.redis_client.hgetall(session_id)
        else:
            scope['session'] = {}

        async def send_wrapper(message):
            nonlocal session_id  # Ensure session_id is accessible here
            if message['type'] == 'http.response.start':
                if scope['session']:
                    if not session_id:
                        session_id = str(uuid.uuid4())
                        scope['headers'].append((b'Set-Cookie', f'session_id={session_id}'.encode()))
                    await self.redis_client.hmset(session_id, scope['session'])
            await send(message)

        await self.app(scope, receive, send_wrapper)
