# @Time    : 2020-05-14 15:45
# @Author  : Seven
# @File    : serializers.py
# @Desc    : ORM Serializer


from typing import Any

from pydantic import BaseModel
from tortoise import Model
from tortoise.fields.relational import BackwardFKRelation

NOT_META = 'Must set model class under Meta class'
NOT_TORTOISE_CLASS = 'model must be an instance of tortoise.Model'
NOT_INSTANCE = 'Cannot serialize; class not instantiated with tortoise.Model'
NOT_ONLY_REQUIRED = 'May not set both `exclude` and `fields`'


class BaseSerializer:
    __slots__ = ['instance', 'model', 'fields_map', '_fields', 'exclude', 'fields', '_data']

    def __init__(self, instance: Model = None):
        meta = getattr(self, 'Meta', None)
        model = getattr(meta, 'model', None)
        assert meta and model, NOT_META
        assert issubclass(model, Model), NOT_TORTOISE_CLASS

        self.instance: Model = instance
        self.model = model
        self.fields_map = getattr(model, '_meta', None).fields_map
        self.exclude = getattr(meta, 'exclude', ())
        self.fields = getattr(meta, 'fields', ())

        self._fields = self.set_fields()
        self._data = self._serialize()

    def set_fields(self) -> list:
        if self.fields:
            return [
                key for key, value in self.fields_map.items()
                if key in self.fields and not isinstance(value, BackwardFKRelation)
            ]
        else:
            return [
                key for key, value in self.fields_map.items()
                if key not in self.exclude and not isinstance(value, BackwardFKRelation)
            ]

    @property
    def data(self) -> dict:
        return self._data

    def _serialize(self) -> dict:
        assert self.instance, NOT_INSTANCE
        return {key: getattr(self.instance, key) for key in self._fields}


class AutoSerializer:
    __slots__ = ['serializer', 'queryset', '_data']
    _base_meta = None

    def __init__(self, queryset: Any):
        meta = getattr(self, 'Meta', None)
        if self._base_meta is None:
            self._set_base_meta(meta)

        assert meta, NOT_META
        self.serializer = BaseSerializer
        setattr(self.serializer, 'Meta', meta)
        self.queryset = queryset
        self._data = None

    @classmethod
    def _set_base_meta(cls, meta: type):
        AutoSerializer._base_meta = type('Mate', (object,), dict())
        AutoSerializer._base_meta.model = getattr(meta, 'model', None)
        AutoSerializer._base_meta.exclude = getattr(meta, 'exclude', ())
        AutoSerializer._base_meta.fields = getattr(meta, 'fields', ())

    def reduction_meta(self):
        self._meta_setattr('fields', AutoSerializer._base_meta.fields)
        self._meta_setattr('exclude', AutoSerializer._base_meta.exclude)

    @property
    def data(self) -> list or dict:
        if self._data:
            return self._data
        self.reduction_meta()
        self._serialize()
        return self._data

    def _serialize(self):
        if isinstance(self.queryset, list):
            self._data = []
            for item in self.queryset:
                self._data.append(self.serializer(item).data)
        else:
            self._data = self.serializer(self.queryset).data

    def _meta_setattr(self, name: str, value: Any):
        meta = getattr(self.serializer, 'Meta', None)
        setattr(meta, name, value)

    def exclude(self, exclude_set: tuple):
        self._meta_setattr('exclude', exclude_set)
        self._serialize()
        return self

    def fields(self, field_set: tuple):
        self._meta_setattr('fields', field_set)
        self._serialize()
        return self


class AutoModelSerializer(BaseModel):
    _exclude = ()
    _fields = ()

    def __init__(self, **data: Any) -> None:
        super(AutoModelSerializer, self).__init__(**data)

    def set_fields(self, field_set: tuple):
        AutoModelSerializer._fields = field_set
        return self

    def exclude(self, exclude_set: tuple):
        AutoModelSerializer._exclude = exclude_set
        return self

    def _set_fields(self) -> list:
        if self._fields:
            return [key for key, value in self.__dict__.items() if key in AutoModelSerializer._fields]
        else:
            return [key for key, value in self.__dict__.items() if key not in AutoModelSerializer._exclude]

    def data(self):
        fields_list = self._set_fields()
        return {key: self.__dict__[key] for key in fields_list}


__all__ = ['AutoSerializer', 'AutoModelSerializer']
