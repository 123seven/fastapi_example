# @Time    : 2020/12/16 5:06 下午
# @Author  : Seven
# @File    : example
# @Desc    :

from fastapi import APIRouter, Request
from loguru import logger
from tortoise import Tortoise

router = APIRouter()


@router.get('/example', summary='示例')
async def example(request: Request):
    # db 使用
    conn = Tortoise.get_connection('default')
    data = await conn.execute_query_dict("SELECT VERSION()")
    logger.debug(f"execute_query_dict:{data}")

    # redis 使用
    await request.app.state.redis.set("fastapi_example:run", 1, expire=10)
    return 'ok'
