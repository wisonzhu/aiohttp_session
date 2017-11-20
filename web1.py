#!/usr/bin/env python
# encoding: utf-8
import asyncio
import time
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_session.redis_storage import RedisStorage
from aioredis import create_pool
from aiohttp_session import redis_storage, setup

async def handler(request):
    session = await get_session(request)
    print(session)
    session['last_visit'] = 'session value'
    return web.Response(body='OK')

async def init(loop):
    app = web.Application()
    redis = await create_pool(('localhost', 6379))
    setup(app, RedisStorage(redis,cookie_name="testmyid",max_age=3))
    app.router.add_route('GET', '/', handler)
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', 8084)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
