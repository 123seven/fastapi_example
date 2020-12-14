# @Time    : 2020/12/7 1:49 下午
# @Author  : Seven
# @File    : exception
# @Desc    : 异常处理

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request


async def http_error_handler(_: Request, exc: HTTPException) -> ORJSONResponse:
    """ http异常处理 """
    response_data = {'code': exc.status_code * 100, 'message': '错误 | Fail', 'error': exc.detail}
    return ORJSONResponse(response_data)


async def validation_error_handler(_: Request, exc: RequestValidationError) -> ORJSONResponse:
    """ 参数验证异常处理 """
    response_data = {
        'code': 422, 'message': '参数错误 | Fail',
        'error': exc.errors()[0]['msg'] if exc.errors() else '', 'error_info': exc.errors(),
        "body": exc.body,
    }
    return ORJSONResponse(response_data)


__all__ = ['http_error_handler', 'validation_error_handler']
