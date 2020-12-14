# @Time    : 2020/12/10 1:45 下午
# @Author  : Seven
# @File    : log
# @Desc    :

import logging

from fastapi import FastAPI


def init_logging(app: FastAPI, add_exception_handlers: bool = False) -> None:
    @app.on_event("startup")
    async def startup_event() -> None:
        logger = logging.getLogger("uvicorn.access")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            fmt='[%(asctime)s %(filename)s:%(lineno)d %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(handler)

    if add_exception_handlers:
        """ TODO: 此处应实现异常捕获 """
        pass
