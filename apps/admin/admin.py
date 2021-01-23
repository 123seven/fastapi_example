# @Time    : 2020-05-18 16:19
# @Author  : Seven
# @File    : admin.py
# @Desc    : 管理员相关操作
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi import HTTPException
from fastapi.params import Query, Body
from loguru import logger
from tortoise.queryset import Q

from models.admin import Admin
from schemas.admin import AdminModel, AdminUpdateModel
from utils import success_response, parameter_error_response
from utils.depends.authentication import get_token
from utils.tools.paginator import paginator

router = APIRouter()
login_router = APIRouter()


async def check_admin(admin_id: int) -> Admin:
    """
    检查管理员是否存在
    :param admin_id: 管理员ID
    :return: model obj
    """
    result = await Admin.get_or_none(id=admin_id, deleted=False)
    if not result:
        raise HTTPException(400, '账号不存在')
    if not result.enabled:
        raise HTTPException(400, '账号已被禁用，请联系管理员')
    return result


@router.get('', summary='获取admin列表')
async def lists(
        user_info: str = Query(None, description='account or nickname 模糊查询'),
        admin_type: str = Query(None, description='管理员类型过滤'),
        page: int = Query(1, description='page'),
        page_size: int = Query(15, description='page_size'),
):
    result = Admin.filter(deleted=False).order_by('id')
    # account or nickname 模糊查询
    if user_info:
        result = result.filter(Q(account__icontains=user_info) | Q(nickname__icontains=user_info))
    # 管理员类型过滤
    if admin_type:
        result = result.filter(type=admin_type)

    data = await paginator(result, page, page_size)
    count = await result.count()
    return success_response([item.excludes(('password',)).data for item in data], {'count': count})


@router.post('', summary='创建admin')
async def create(request: Request, admin: AdminModel = Body(..., )):
    if request.user.type != 0:
        return parameter_error_response('权限不够，无法创建管理员账号')
    result = await Admin.get_or_none(account=admin.account, enabled=True, deleted=False)
    if result:
        raise HTTPException(400, '账号已存在')
    data = admin.dict(exclude_unset=True)
    data.setdefault('type', 1)
    r = await Admin.create(**data)
    r.set_password(admin.password)
    r.last_at = datetime.now()
    await r.save(update_fields=['password', 'last_at', 'type'])
    return success_response(r.data)


@router.get('/{admin_id}', summary='获取admin详情')
async def retrieve(admin_id: int):
    result = await check_admin(admin_id)
    result.excludes(('password', 'updated_at'))
    return success_response(result.data)


@router.put('/{admin_id}/enabled', summary='admin禁用')
async def enabled(admin_id: int):
    result = await Admin.get_or_none(id=admin_id, deleted=False)
    if not result:
        raise HTTPException(400, '账号不存在')
    if result.enabled:
        result.enabled = False
    else:
        result.enabled = True
    await result.save()
    return success_response()


@router.put('/{admin_id}', summary='更新admin信息')
async def update(request: Request, admin_id: int, admin: AdminUpdateModel = Body(..., )):
    result = await check_admin(admin_id)
    # 不是超级管理员 不是自己的账号不能修改
    if request.user.type != 0:
        if request.user.pk != result.pk:
            return parameter_error_response('权限不够，不能修改他人账号信息')
    # 使用 dict update 更新
    result.__dict__.update(**admin.dict(exclude_unset=True))
    # 密码修改
    data = admin.dict(exclude_unset=True)
    if data.get('password'):
        result.set_password(data.get('password'))
        data.pop('password')

    await result.save()
    result.excludes(('password',))
    return success_response(result.data)


@router.delete('/{admin_id}', summary='删除admin信息')
async def delete(request: Request, admin_id: int):
    if request.user.type != 0:
        return parameter_error_response('权限不够，无法删除管理员账号')
    instance = await check_admin(admin_id)
    if instance.type == 0:
        return parameter_error_response('无法删除超级管理员')

    instance.deleted = True
    await instance.save(update_fields=['deleted'])
    return success_response('删除成功')


@login_router.post('/login', summary='管理员登录')
async def login(account: str = Body(..., title='账号'), password: str = Body(..., title='密码')):
    result = await Admin.get_or_none(account=account, deleted=False)
    if not result:
        raise HTTPException(400, '账号不存在')
    if result.enabled is not True:
        raise HTTPException(400, '账号已经被禁用，请联系超级管理员')
    try:
        if not result.check_password(password):
            raise HTTPException(400, '密码错误，请检查')
    except Exception as e:
        logger.error(e)
        raise HTTPException(400, '密码错误，请检查')
    result.last_at = datetime.now()
    await result.save(update_fields=['last_at'])
    data = result.excludes(('password', 'deleted')).data
    data.setdefault('token', get_token(result.pk))
    return success_response(data)
