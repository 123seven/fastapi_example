# @Time    : 2020/12/4 1:48 下午
# @Author  : Seven
# @File    : redis
# @Desc    :

from aioredis import Redis
from aioredis import create_redis_pool
from fastapi import FastAPI

from conf.config import config


def init_redis(app: FastAPI, add_exception_handlers: bool = False) -> None:
    """
    redis连接池初始化
    """

    async def get_redis_pool() -> Redis:
        return await create_redis_pool(config.REDIS_URI)

    @app.on_event("startup")
    async def startup_redis_event() -> None:
        """ 获取redis poll使用request.app.state.redis即可直接调用"""
        app.state.redis = await get_redis_pool()

    @app.on_event("shutdown")
    async def shutdown_redis_event() -> None:
        """ 关闭 redis poll """
        if app.state.redis:
            app.state.redis.close()
            await app.state.redis.wait_closed()

    if add_exception_handlers:
        """ TODO: 此处应实现异常捕获 """
        pass
