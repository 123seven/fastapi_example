# @Time    : 2021/1/20 2:48 下午
# @Author  : Seven
# @File    : scheduler
# @Desc    : 调度器

from collections import OrderedDict

from apscheduler.jobstores.base import JobLookupError
from apscheduler.util import datetime_to_utc_timestamp
from fastapi import APIRouter, Body, Query

from schemas.scheduler import SchedulerModel
from utils import success_response, parameter_error_response
from utils.tools import task_scheduler, default_job_stores

router = APIRouter()


@router.get('/record', summary='任务执行记录')
async def tasks(
        page: int = Query(1, description='page'),
        page_size: int = Query(15, description='page_size'),
):
    # 分页
    offset = (page - 1) * page_size
    limit = page_size
    # 处理一下格式
    data_list = []
    for item in default_job_stores.get_record(offset=offset, limit=limit):
        data_list.append(OrderedDict({
            'id': item.values()[0],
            'run_time': item.values()[1],
            'name': item.values()[2],
            'status': item.values()[3],
        }))

    return success_response(data_list)


@router.get('', summary='任务列表')
async def lists():
    data_list = []
    for job in task_scheduler.get_jobs():
        data_list.append({
            'job_id': job.id,
            'name': job.name,
            'next_run_time': int(datetime_to_utc_timestamp(job.next_run_time)),
            'trigger': job.__getstate__().get('trigger').__class__.__name__,
            'args': job.args,
            'kwargs': job.kwargs,
        })
    return success_response(data_list)


@router.post('/add', summary='添加任务')
async def add(model: SchedulerModel = Body(..., )):
    print(model.__dict__)
    job = task_scheduler.add_job(**model.__dict__)

    return success_response({
        'job_id': job.id,
        'name': job.name,
        'next_run_time': int(datetime_to_utc_timestamp(job.next_run_time)),
        'trigger': job.__getstate__().get('trigger').__class__.__name__,
        'args': job.args,
        'kwargs': job.kwargs,
    })


@router.delete('/{job_id}/remove', summary='删除任务')
async def remove(job_id: str):
    try:
        task_scheduler.remove_job(job_id)
    except JobLookupError:
        return parameter_error_response("删除任务失败")
    return success_response()


@router.put('/{job_id}/pause', summary='暂停任务')
async def pause(job_id: str):
    try:
        task_scheduler.pause_job(job_id)
    except JobLookupError:
        return parameter_error_response("暂停任务失败")
    return success_response()


@router.put('/{job_id}/resume', summary='恢复任务')
async def remove(job_id: str):
    try:
        task_scheduler.resume_job(job_id)
    except JobLookupError:
        return parameter_error_response("恢复任务失败")
    return success_response()
