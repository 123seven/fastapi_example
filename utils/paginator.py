# @Time    : 2020-05-18 17:08
# @Author  : Seven
# @File    : paginator.py
# @Desc    : 分页功能


async def paginator(qs, page: int = 1, page_size: int = 15) -> list:
    offset = (page - 1) * page_size
    limit = page_size
    return await qs.offset(offset).limit(limit)
