# @Time    : 2020-06-08 09:29
# @Author  : Seven
# @File    : enum.py
# @Desc    : 枚举choices实现

import abc


class EnumMixin:
    @classmethod
    @abc.abstractmethod
    def choices(cls):
        pass
