# @Time    : 2020-05-18 16:19
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : Admin router


from fastapi import APIRouter, Depends

from utils.authentication import jwt_authentication
from . import admin as router_admin

admin_router = APIRouter()

admin_router.include_router(
    router_admin.login_router,
    prefix='/admin',
    tags=['admin']
)
# jwt 认证
admin_router.include_router(
    router_admin.router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(jwt_authentication)],
)
