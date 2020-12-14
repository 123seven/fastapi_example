# @Time    : 2020/11/12 3:58 下午
# @Author  : Seven
# @File    : rbac
# @Desc    : rbac 权限相关
import re

from fastapi import FastAPI, Request, HTTPException

# 需要排除的路由

router_exclude: list = ['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc']


def get_router(application: FastAPI) -> list:
    """
    获取路由path
    """
    routes = []
    for i in application.router.routes:
        if i.path not in router_exclude:
            routes.append({
                "path": i.__dict__.get('path_regex').pattern,
                "methods": i.methods.pop(),
                "summary": i.__dict__.get('summary'),
                "tags": i.__dict__.get('tags').pop(),
            })
    return routes


async def rbac_check(request: Request) -> None:
    """
    rbac 权限检查
    """
    # 检查权限
    path = request.scope.get("path")
    for role in await request.user.role:
        for permissions in await role.permissions:
            if re.match(permissions.path, path) and request.scope.get("method") == permissions.method:
                return

    raise HTTPException(401, '权限不足')


__all__ = ['get_router', 'rbac_check']
