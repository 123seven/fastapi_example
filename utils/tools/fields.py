# @Time    : 2020-06-08 17:18
# @Author  : Seven
# @File    : fields.py
# @Desc    : fields 重写
import collections
import datetime
from typing import Optional, Any

from tortoise.fields import SmallIntField, DatetimeField


class ChoicesField(SmallIntField):
    def __init__(self, choices: tuple, description: Optional[str] = None, **kwargs: Any) -> None:
        if isinstance(choices, collections.abc.Iterator):
            choices = list(choices)
        super().__init__(description=description, **kwargs)
        self.choices = dict(choices)


def get_choices_field(choices: tuple) -> str:
    _str = ''
    for k, v in dict(choices).items():
        _str += f'{k}:{v} '
    return _str


class LocalDatetimeField(DatetimeField):
    def to_db_value(
            self, value: Optional[datetime.datetime], instance: "Union[Type[Model], Model]") -> Optional[datetime.datetime]:
        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
                self.auto_now
                or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = datetime.datetime.now()
            setattr(instance, self.model_field_name, value)
            return value
        return value


__all__ = ['ChoicesField', 'LocalDatetimeField', 'get_choices_field']
