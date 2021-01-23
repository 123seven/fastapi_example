# @Time    : 2021/1/20 2:03 下午
# @Author  : Seven
# @File    : apscheduler
# @Desc    :


from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.util import datetime_to_utc_timestamp
from fastapi import FastAPI

from tests.scheduler_test import run_test

try:
    import cPickle as pickle
except ImportError:  # pragma: nocover
    import pickle

try:
    from sqlalchemy import (Table, Column, MetaData, Unicode, Float, SmallInteger, Integer, select, and_)
    from sqlalchemy.exc import IntegrityError
except ImportError:  # pragma: nocover
    raise ImportError('SQLAlchemyJobStore requires SQLAlchemy installed')


class JobStore(SQLAlchemyJobStore):
    """ 继承SQLAlchemyJobStore 增加add_record记录执行历史 """
    record_t = Table(
        'scheduler_record', MetaData(),
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('run_time', Float(25)),
        Column('name', Unicode(128), nullable=True),
        Column('status', SmallInteger, nullable=False, default=1, comment="1:成功 2:失败 3:异常"),
    )

    def start(self, scheduler, alias):
        super(SQLAlchemyJobStore, self).start(scheduler, alias)
        self.jobs_t.create(self.engine, True)
        self.record_t.create(self.engine, True)

    def add_record(self, next_run_time, job_name, status=1):
        """ 添加执行记录 """
        insert = self.record_t.insert().values(**{
            'run_time': datetime_to_utc_timestamp(next_run_time),
            'name': job_name,
            'status': status,
        })
        try:
            self.engine.execute(insert)
        except IntegrityError as e:
            print(e)

    def get_record(self, *conditions, offset: int = 0, limit: int = 15):
        """ 获取执行记录 """
        selectable = select([
            self.record_t.c.id, self.record_t.c.run_time, self.record_t.c.name, self.record_t.c.status]
        ).order_by(self.record_t.c.id).limit(limit)
        selectable = selectable.where(and_(*conditions)) if conditions else selectable
        # 优化分页
        selectable = selectable.where(self.record_t.c.id > offset)
        jobs_record = self.engine.execute(selectable)
        return jobs_record


# init scheduler
default_job_stores: JobStore = JobStore(url="sqlite:///jobs.sqlite")
job_stores = {
    'default': default_job_stores
}
task_scheduler: BackgroundScheduler = BackgroundScheduler(jobstores=job_stores)


def scheduler_listener(event: JobExecutionEvent) -> None:
    """ 监听器 记录执行历史 """
    job = task_scheduler.get_job(event.job_id)
    default_job_stores.add_record(event.scheduled_run_time, job.name, 1 if event.code == EVENT_JOB_ERROR else 2)


def init_scheduler(app: FastAPI, add_exception_handlers: bool = False) -> None:
    """
    init_scheduler初始化
    """

    @app.on_event("startup")
    async def startup_scheduler_event() -> None:
        """ 启动 scheduler """
        # 添加一个测试任务
        task_scheduler.add_job(run_test, name='test_task', trigger="interval", hours=2)
        # 监听任务执行
        task_scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        # 启动定时任务
        task_scheduler.start()

    @app.on_event("shutdown")
    async def shutdown_scheduler_event() -> None:
        """ 关闭 scheduler """
        # 清空所有任务 可根据自己的业务场景来选择是清空还是暂停等
        default_job_stores.remove_all_jobs()
        default_job_stores.shutdown()
        task_scheduler.shutdown()

    if add_exception_handlers:
        """ TODO: 此处应实现异常捕获 """
        pass


__all__ = ['default_job_stores', 'task_scheduler', 'init_scheduler', ]
