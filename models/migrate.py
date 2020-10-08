# @Time    : 2020-05-15 08:58
# @Author  : Seven
# @File    : migrate.py
# @Desc    : migrate table

from tortoise import Tortoise, run_async

from conf.config import config
from models.admin import Admin


async def migrate():
    await Tortoise.init(
        db_url=config.DATABASE_URL,
        modules=config.MODELS,
    )
    await Tortoise.generate_schemas()

    print("Success migration!")


async def create_super_admin(account='super_admin', password='12345'):
    await Tortoise.init(
        db_url=config.DATABASE_URL,
        modules=config.MODELS,
    )
    await Admin.create_super_admin(account, password)
    print("Success create super admin!")


if __name__ == '__main__':
    run_async(migrate())
    run_async(create_super_admin())
