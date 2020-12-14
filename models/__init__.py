# @Time    : 2020-05-18 14:55
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : 数据库
import decimal
from collections import OrderedDict
from typing import Any

from fastapi import FastAPI
from tortoise import BackwardFKRelation, QuerySet
from tortoise import fields, Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.fields import ManyToManyRelation
from tortoise.fields.relational import NoneAwaitable

from conf.config import config
from utils.tools.fields import LocalDatetimeField


def init_db(app: FastAPI):
    """ 连接数据库
    """
    register_tortoise(
        app,
        db_url=config.DATABASE_URL,
        modules=config.MODELS,
        add_exception_handlers=True,
    )


class BaseModelMixin(Model):
    """
    基础模型表，用于给其他Model集成
    """
    created_at = LocalDatetimeField(auto_now_add=True, description='创建时间')
    updated_at = LocalDatetimeField(auto_now=True, description='修改时间')
    deleted = fields.BooleanField(default=False, description="是否删除")

    class Meta:
        abstract = True

    def __init__(self, **kwargs: Any) -> None:

        meta = getattr(self, 'Meta', None)
        self.__dict__.setdefault('_exclude', getattr(meta, 'exclude', ()))
        self.__dict__.setdefault('_fields', getattr(meta, 'fields', ()))

        super(BaseModelMixin, self).__init__(**kwargs)

    def excludes(self, exclude_set: tuple):
        self.__dict__['_exclude'] = exclude_set
        return self

    def fields(self, field_set: tuple):
        self.__dict__['_fields'] = field_set
        return self

    def set_fields(self) -> list:
        _fields = self.__dict__.get('_fields', ())
        fields_map = getattr(self, '_meta', None).fields_map
        if _fields:
            return [
                key for key, value in fields_map.items()
                if key in _fields and not isinstance(value, BackwardFKRelation)
            ]
        else:
            _exclude = self.__dict__.get('_exclude', ())
            return [
                key for key, value in fields_map.items()
                if key not in _exclude and not isinstance(value, BackwardFKRelation)
            ]

    @property
    def data(self) -> dict:
        return self._serialize()

    async def get_data(self) -> dict:
        return await self._async_serialize()

    async def _async_serialize(self) -> dict:
        field_list = self.set_fields()
        data = OrderedDict()
        for key in field_list:
            if hasattr(self, f'get_{key}'):
                value = getattr(self, f'get_{key}')()
            else:
                value = getattr(self, key)
            # 如果返回的是model类型就异步调用之前定义好的方法
            if isinstance(value, (Model, ManyToManyRelation, QuerySet, NoneAwaitable.__class__)):
                value = await getattr(self, f'async_get_{key}')()
            if isinstance(value, decimal.Decimal):
                value = str(value)
            data.setdefault(key, value)
        return data

    def _serialize(self) -> dict:
        field_list = self.set_fields()
        data = OrderedDict()
        for key in field_list:
            if hasattr(self, f'get_{key}'):
                value = getattr(self, f'get_{key}')()
            else:
                value = getattr(self, key)
            if isinstance(value, decimal.Decimal):
                value = str(value)
            if isinstance(value, (Model, ManyToManyRelation, QuerySet, NoneAwaitable.__class__)):
                value = None
            data.setdefault(key, value)
        return data

    def __str__(self) -> str:
        if self.pk:
            return f"<{self.__class__.__name__}: {self.pk}>"
        return f"<{self.__class__.__name__}>"

    def get_created_at(self) -> str or None:
        if not self.created_at:
            return self.created_at
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self) -> str or None:
        if not self.updated_at:
            return self.updated_at
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')


__all__ = ['init_db', 'BaseModelMixin', ]
