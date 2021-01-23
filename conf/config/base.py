# @Time    : 2020-05-18 15:23
# @Author  : Seven
# @File    : base.py
# @Desc    : 基础配置


import os
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目名称
PROJECT_NAME: str = os.environ.get('PROJECT_NAME') or 'fastapi_example'
# 是否开启debug模式
DEBUG: bool = os.environ.get('DEBUG') or True
# 项目版本
VERSION: str = os.environ.get('VERSION') or '0.0.1'

# CORS 配置
ALLOWED_HOSTS: List[str] = ['*']
ALLOWED_METHODS: List[str] = ['*']
ALLOWED_HEADERS: List[str] = ['*']

# 数据库链接配置
DATABASE_URL: str = os.environ.get('DATABASE_URL') or 'mysql://root:fastapi_example.2020@mysql:3306/fastapi_example'

# 数据库使用那些model配置
MODELS: Dict[str, List[str]] = {'models': ['models.admin', ]}

# jwt token 设置
SECRET_KEY: str = '09d25q3e094faa6ca2w556c818wqy313f7099f6f0f4caa6cf63b88e8r53d3e7'
ALGORITHM: str = "HS256"

# 是否开启定时任务
SCHEDULER_USE: bool = os.environ.get('SCHEDULER_USE') or False
