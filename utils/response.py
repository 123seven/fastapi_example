# @Time    : 2020-05-06 16:57
# @Author  : Seven
# @File    : response.py
# @Desc    : Response
from typing import Any

import orjson
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response, RedirectResponse
from pydantic import BaseModel
from starlette.requests import Request


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> orjson:
        return orjson.dumps(
            content
        )


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    response_data = {'code': exc.status_code * 100, 'message': '错误 | Fail', 'error': exc.detail}
    return JSONResponse(response_data)


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    response_data = {'code': 422, 'message': '参数错误 | Fail', 'error': exc.errors(), "body": exc.body}
    return JSONResponse(response_data)


class Default(BaseModel):
    code: int
    message: str or None = None


def success_response(data: Any = None, kwargs: dict = None) -> JSONResponse:
    """
    Success Response
    :param data: response data
    :param kwargs: update JSON Response kwargs
    :return: JSONResponse
    """
    response_data = {'code': 0, 'message': '成功 | Success'}
    if data is not None:
        response_data['data'] = data
    if kwargs:
        response_data.update(kwargs)
    return JSONResponse(response_data)


def parameter_error_response(error: str = None, kwargs: dict = None) -> JSONResponse:
    """
    Parameter Error Response
    :param error: error str
    :param kwargs: update JSON Response kwargs
    :return: JSONResponse
    """
    response_data = {'code': 40000, 'message': '参数错误 | Fail'}
    if error:
        response_data['error'] = error
    if kwargs:
        response_data.update(kwargs)
    return JSONResponse(response_data, status_code=200)


def server_error_response(error: str = None, kwargs: dict = None) -> JSONResponse:
    """
    Server Error Response
    :param error: error str
    :param kwargs: update JSON Response kwargs
    :return: JSONResponse
    """
    response_data = {'code': 50000, 'message': '服务器错误 | Fail'}
    if error:
        response_data['error'] = error
    if kwargs:
        response_data.update(kwargs)
    return JSONResponse(response_data, status_code=500)


__all__ = ['success_response', 'parameter_error_response', 'server_error_response', 'http_error_handler', 'Default',
           'validation_error_handler']
