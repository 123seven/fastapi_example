# @Time    : 2020-06-23 17:37
# @Author  : Seven
# @File    : redis_pool.py
# @Desc    : redis pool

from loguru import logger
from redis.sentinel import Sentinel

from conf.config import config

MY_SENTINEL = None
MASTER = None
SLAVE = None


# 1.redis 哨兵模式集群最少需要一主三从, 三哨兵
# 2.redis 哨兵集群所有主从节点都完整的保存了一份数据


def parse() -> list:
    """解析redis哨兵配置
    """
    sentinel_address_str = config.SENTINEL_ADDRESS
    sentinel_address_list = sentinel_address_str.split(",")
    sentinel_address_list = [tuple(item.split(":")) for item in sentinel_address_list]
    logger.info(f"SENTINEL_ADDRESS_STR:{sentinel_address_str}", )
    logger.info(f"SENTINEL_ADDRESS:{sentinel_address_list}", )

    return sentinel_address_list


def get_redis_conn():
    global MY_SENTINEL
    global MASTER
    global SLAVE

    sentinel_address = parse()

    # 如果哨兵连接实例已存在, 不重复连接, 当连接失效时, 重新连接
    if not MY_SENTINEL:  # 连接哨兵
        MY_SENTINEL = Sentinel(sentinel_address, socket_timeout=2000)  # 尝试连接最长时间单位毫秒, 1000毫秒为1秒
        # 通过哨兵获取主数据库连接实例      参数1: 主数据库的名字(集群部署时在配置文件里指明)
        MASTER = MY_SENTINEL.master_for('mymaster', socket_timeout=2000)
        # 通过哨兵获取从数据库连接实例    参数1: 从数据的名字(集群部署时在配置文件里指明)
        SLAVE = MY_SENTINEL.slave_for('mymaster', socket_timeout=2000)


# 每次都先尝试生成连接实例
get_redis_conn()

__all__ = ['MASTER', 'SLAVE', ]
