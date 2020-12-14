# @Time    : 2020-05-14 09:24
# @Author  : Seven
# @File    : authentication.py
# @Desc    : jwt token
import datetime

import jwt
from fastapi import Request, Header, HTTPException
from jwt.exceptions import DecodeError, ExpiredSignatureError

from conf.config import config
from models.admin import Admin


async def jwt_authentication(request: Request, authorization: str = Header(None, description='token')) -> None:
    """
    jwt token认证
    将方法加入到需要认证的路由上即可实现认证
    :param request:  request
    :param authorization: token str
    """
    if authorization:
        try:
            user = get_token_data(authorization)
            result = await Admin.get_or_none(id=user['user_id'], deleted=False)
            if not result:
                raise HTTPException(403, '账号不存在')
            if result.enabled is False:
                raise HTTPException(200, '账号已被禁用，请联系管理员')
            # 权限检查
            await request.scope.setdefault('user', result)
            return
        except (KeyError, TypeError, DecodeError, ExpiredSignatureError):
            raise HTTPException(403, 'TOKEN错误')
    else:
        raise HTTPException(403, 'TOKEN不存在')


def get_token(user_pk: int, _type: str = 'admin', expiration: int = 60 * 60 * 24 * 5) -> str:
    """
    获取token
    :param user_pk: 用户主键
    :param _type: 用户类型 admin or user
    :param expiration: 过期时间，默认5天
    :return: jwt token str
    """
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    to_encode = {'user_id': user_pk, 'type': _type, 'exp': expire}
    return jwt.encode(to_encode, config.SECRET_KEY + _type, algorithm=config.ALGORITHM).decode()


def get_token_data(token: str, _type: str = 'admin') -> dict:
    """
    token返回data
    :param token: jwt token
    :param _type: 用户类型 admin or user
    :return: data dict
    """
    return jwt.decode(token, config.SECRET_KEY + _type, algorithms=[config.ALGORITHM])


def set_data(data: dict, expiration: int = 7200) -> str:
    """ 加密一个dict数据 """
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    to_encode = {'exp': expire}
    to_encode.update(**data)
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM).decode()


def get_data(key: str) -> dict:
    """解密一个key """
    return jwt.decode(key, config.SECRET_KEY, algorithms=[config.ALGORITHM])


__all__ = ['get_token', 'get_token_data', 'jwt_authentication', 'set_data', 'get_data']
