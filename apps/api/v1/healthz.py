# @Time    : 2020/12/1 10:02 上午
# @Author  : Seven
# @File    : example
# @Desc    : 测试
from fastapi import APIRouter
from tortoise import Tortoise
router = APIRouter()


@router.get('/healthz/', summary='健康检查')
async def monitor():
    conn = Tortoise.get_connection('default')
    return 'ok'
