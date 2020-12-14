# @Time    : 2020-05-18 16:25
# @Author  : Seven
# @File    : admin.py
# @Desc    : admin model

from passlib.context import CryptContext
from tortoise import fields

from models import BaseModelMixin
from utils.tools.fields import LocalDatetimeField

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(BaseModelMixin):
    """
    用户表
    """
    account = fields.CharField(max_length=32, unique=True, null=True, description='管理员账号')
    password = fields.CharField(max_length=128, null=True, description='密码')

    nickname = fields.CharField(max_length=32, null=True, description='管理员昵称')
    avatar_url = fields.CharField(max_length=255, null=True, description='头像URL')
    wechat_id = fields.CharField(max_length=32, null=True, description='微信号')
    real_name = fields.CharField(max_length=32, null=True, description='真实姓名')
    email = fields.CharField(max_length=32, null=True, description='邮箱')
    mobile = fields.CharField(max_length=30, null=True, description='手机号码')

    enabled = fields.BooleanField(default=True, description="启用")
    type = fields.IntField(description='管理员类型0:超级管理员1:管理员')
    last_at = LocalDatetimeField(null=True, description='最后登录时间')
    remark = fields.CharField(max_length=255, null=True, description='备注')
    role: fields.ManyToManyRelation["Role"] = fields.ManyToManyField(
        "models.Role", related_name="user", null=True, description="角色"
    )

    class Meta:
        exclude = ('password',)

    def set_password(self, password: str):
        """ 设置加密密码
        :param password: 明文密码
        """
        self.password = pwd_context.hash(password)

    def check_password(self, raw_password: str) -> bool:
        """ 检查密码是否正确
        :param raw_password: 明文密码
        :return: bool
        """
        return pwd_context.verify(raw_password, self.password)

    @staticmethod
    async def create_super_admin(account='super_admin', password='12345') -> 'Admin':
        """ 创建超级管理员
        :param account: str 管理员账号
        :param password: str 密码
        :return: admin obj
        """
        instance = await Admin.get_or_none(account=account, type=0)
        if not instance:
            instance = await Admin.create(account=account, type=0, password='0')
        instance.set_password(password)
        await instance.save(update_fields=['password'])
        return instance

    def get_created_at(self) -> str or None:
        if not self.created_at:
            return self.created_at
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self) -> str or None:
        if not self.updated_at:
            return self.updated_at
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_last_at(self) -> str or None:
        if not self.last_at:
            return self.last_at
        return self.last_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_avatar_url(self) -> str:
        if self.avatar_url:
            return self.avatar_url
        return 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'


class Permission(BaseModelMixin):
    """
    权限
    """
    name = fields.CharField(max_length=64, null=True, description='操作名称')
    method = fields.CharField(max_length=50, null=True, description="方法")
    path = fields.CharField(max_length=255, null=True, description='path')
    tags = fields.CharField(max_length=64, null=True, description='标签')
    remark = fields.CharField(max_length=255, null=True, description='备注')


class Role(BaseModelMixin):
    """
    角色表
    """
    name = fields.CharField(max_length=255, null=True, description='角色名称')
    status = fields.IntField(default=1, description="角色状态 0:禁用 1:启用")
    permissions: fields.ManyToManyRelation["Permission"] = fields.ManyToManyField(
        "models.Permission", related_name="role", null=True, description="权限")
    remark = fields.CharField(max_length=255, null=True, description='备注')
