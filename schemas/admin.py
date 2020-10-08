# @Time    : 2020-05-19 13:06
# @Author  : Seven
# @File    : admin.py
# @Desc    : admin schema


from pydantic import Field

from utils.serializers import AutoModelSerializer


class AdminModel(AutoModelSerializer):
    account: str = Field(max_length=32, description='管理员账号')
    password: str = Field(max_length=128, description='密码')
    nickname: str = Field(None, max_length=32, null=True, description='管理员昵称')
    avatar_url: str = Field(None, max_length=255, null=True, description='头像URL')
    phone: str = Field(None, max_length=30, null=True, description='手机号码')
    email: str = Field(None, max_length=32, null=True, description='邮箱')
    wechat_id: str = Field(None, max_length=32, null=True, description='微信号')


class AdminUpdateModel(AutoModelSerializer):
    password: str = Field(None, max_length=128, null=True, description='密码')
    nickname: str = Field(None, max_length=32, null=True, description='管理员昵称')
    avatar_url: str = Field(None, max_length=255, null=True, description='头像URL')
    remark: str = Field(None, max_length=255, null=True, description='备注')
    email: str = Field(None, max_length=32, null=True, description='邮箱')
    type: int = Field(None, null=True, description='超级管理员')
    wechat_id: str = Field(None, max_length=32, null=True, description='微信号')
