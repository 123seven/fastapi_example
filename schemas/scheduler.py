# @Time    : 2021/1/20 6:08 下午
# @Author  : Seven
# @File    : scheduler
# @Desc    : Scheduler
from pydantic import BaseModel, Field


class SchedulerModel(BaseModel):
    func: str = Field(max_length=255, description='执行函数', default='tests.scheduler_test:run_test')
    args: list = Field(description='执行参数', default=('HeNan',))
    trigger: str = Field(max_length=128, description='trigger', default='interval')
    seconds: int = Field(description='seconds', default=30)

