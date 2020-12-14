# @Time    : 2020/12/4 1:48 下午
# @Author  : Seven
# @File    : redis
# @Desc    :

import aioredis
from fastapi import FastAPI

from conf.config import config


def init_redis(app: FastAPI, add_exception_handlers: bool = False) -> None:
    """
    redis连接池初始化
    """

    @app.on_event("startup")
    async def create_redis_pool() -> None:
        app.state.redis = await aioredis.create_redis_pool(config.get_conf('REDIS_URI'))

    @app.on_event("shutdown")
    async def close_redis() -> None:
        if app.state.redis:
            app.state.redis.close()
            await app.state.redis.wait_closed()

    if add_exception_handlers:
        """ TODO: 此处应实现异常捕获 """
        pass
