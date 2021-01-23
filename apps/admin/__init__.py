# @Time    : 2020-05-18 16:19
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : Admin router


from fastapi import APIRouter, Depends

from utils.depends.authentication import jwt_authentication
from utils.depends.rbac import rbac_check
from . import admin as router_admin
from . import scheduler as router_scheduler

admin_router = APIRouter()

admin_router.include_router(
    router_admin.login_router,
    prefix='/admin',
    tags=['admin']
)
# jwt认证/rbac权限
admin_router.include_router(
    router_admin.router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(jwt_authentication), Depends(rbac_check)],
)

# scheduler
admin_router.include_router(
    router_scheduler.router,
    prefix='/scheduler',
    tags=['admin'],
    dependencies=[Depends(jwt_authentication), Depends(rbac_check)],
)
