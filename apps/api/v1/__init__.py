# @Time    : 2020-05-18 16:19
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : Api Router

from fastapi import APIRouter

from . import cbv as cbv_router
from . import healthz as healthz_router

api_router = APIRouter()

api_router.include_router(healthz_router.router, prefix='/v1', tags=['v1'])
api_router.include_router(cbv_router.router, prefix='/v1', tags=['v1-cbv'])
