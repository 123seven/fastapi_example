# @Time    : 2020/12/8 5:22 下午
# @Author  : Seven
# @File    : cbv
# @Desc    :


from fastapi import APIRouter, Depends

from utils.tools.cbv import cbv

router = APIRouter()


def dependency() -> int:
    """
    依赖
    """
    return 1


@cbv(router)
class CBV:
    def __init__(self, z: int = Depends(dependency)):
        """
        依赖处理
        """
        self.y = 1
        self.z = z

    @router.get("/cbv", response_model=str, summary="FastAPI CBV实现")
    def get(self) -> str:
        """
        FastAPI CBV实现
        """
        return "ok"

    @router.post("/cbv", response_model=str, summary="FastAPI CBV实现")
    def post(self) -> str:
        """
        FastAPI CBV实现
        """
        return "ok"
