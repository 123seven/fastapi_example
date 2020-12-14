# @Time    : 2020-05-15 08:58
# @Author  : Seven
# @File    : migrate.py
# @Desc    : migrate table

from loguru import logger
from tortoise import Tortoise, run_async

from conf.config import config
from main import app
from models.admin import Admin, Permission, Role
from utils.depends.rbac import get_router


async def migrate() -> None:
    await Tortoise.init(db_url=config.DATABASE_URL, modules=config.MODELS)
    await Tortoise.generate_schemas()
    print("Success migration!")


async def create_super_admin(account: str = 'super_admin', password: str = 'super_admin-12345') -> None:
    # create super admin
    await Tortoise.init(db_url=config.DATABASE_URL, modules=config.MODELS)
    super_admin = await Admin.create_super_admin(account, password)
    print("Success create super admin!")

    # init rbac
    role, is_create = await Role.get_or_create(name="超级管理员")
    for path_info in get_router(app):
        logger.debug(f"create permission :{path_info}")
        permission, is_create = await Permission.get_or_create(
            path=path_info['path'], method=path_info['methods'],
            name=path_info['summary'], tags=path_info['tags'],
        )
        await role.permissions.add(permission)

    await super_admin.role.clear()
    await super_admin.role.add(role)
    print("Success init permission!")


if __name__ == '__main__':
    run_async(migrate())
    run_async(create_super_admin())
