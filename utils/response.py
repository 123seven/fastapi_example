# @Time    : 2020-05-06 16:57
# @Author  : Seven
# @File    : response.py
# @Desc    : Response
from typing import Any

from fastapi.responses import ORJSONResponse
from pydantic import BaseModel


class Default(BaseModel):
    code: int
    message: str or None = None


def success_response(data: Any = None, kwargs: dict = None) -> ORJSONResponse:
    """
    Success Response
    :param data: response data
    :param kwargs: update JSON Response kwargs
    :return: JSONResponse
    """
    response_data = {'code': 20000, 'message': '成功 | Success'}
    if data is not None:
        response_data['data'] = data
    if kwargs:
        response_data.update(kwargs)
    return ORJSONResponse(response_data)


def parameter_error_response(error: str = None, kwargs: dict = None) -> ORJSONResponse:
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
    return ORJSONResponse(response_data, status_code=200)


def server_error_response(error: str = None, kwargs: dict = None) -> ORJSONResponse:
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
    return ORJSONResponse(response_data, status_code=500)


__all__ = ['success_response', 'parameter_error_response', 'server_error_response', 'Default']
