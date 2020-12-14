## 项目说明

 FastApi Restful Api 项目示例


## 关键特性:

- 快速：可与 NodeJS 和 Go 比肩的极高性能（归功于 Starlette 和 Pydantic）。最快的 Python web 框架之一。
- 高效编码：提高功能开发速度约 200％ 至 300％。*
- 更少 bug：减少约 40％ 的人为（开发者）导致错误。*
- 智能：极佳的编辑器支持。处处皆可自动补全，减少调试时间。
- 简单：设计的易于使用和学习，阅读文档的时间更短。
- 简短：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少。
- 健壮：生产可用级别的代码。还有自动生成的交互式文档。
- 标准化：基于（并完全兼容）API 的相关开放标准：OpenAPI (以前被称为 Swagger) 和 JSON Schema。

## 项目技术栈

**Fastapi:**  用于web服务构建  
**Tortoise-orm:** Python异步ORM  
**Orjson:** 最快的Python Json库  
**Uvicorn:** 基于 asyncio 开发的一个轻量级高效的 Web 服务器框架  
**Pydantic:** Python类型提示以及进行数据验证和设置管理  
**Bcrypt:** 用户信息加密  
**docker:** 服务环境构建  
**docker-compose:** 服务环境快速构建  

## 项目结构

```
➜  fastapi_example git:(master) ✗ tree -I '*.pyc|*.log|*__pycache__*|*deploy*'.
.
├── Dockerfile                  docker file部署文件
├── README.md
├── apps                        apps目录
│   ├── __init__.py
│   ├── admin                  管理后台接口
│   │   ├── __init__.py
│   │   └── admin.py
│   └── api                    API接口
│       ├── __init__.py
│       └── v1                 API v1 路由
│           ├── __init__.py
│           └── healthz.py     健康检查
├── conf                        配置文件目录
│   ├── __init__.py
│   └── config
│       ├── __init__.py        载入配置
│       └── base.py            基础配置
├── docker-compose.yml
├── gunicorn_conf.py            gunicorn 配置
├── logs                        log文件夹
├── main.py                     程序入口
├── models                      数据库model
│   ├── __init__.py            model基础类
│   ├── admin.py
│   └── migrate.py            
├── requirements.txt            项目python依赖
├── schemas                     open API schemas 接口请求参数
│   ├── __init__.py
│   └── admin.py
├── tests                       测试用例
│   └── __init__.py
├── update.sh                   更新脚本
└── utils                      
    ├── __init__.py
    ├── depends                 请求依赖处理
    │   ├── __init__.py
    │   ├── authentication.py  用户认证
    │   └── rbac.py            接口权限检查
    ├── exception.py            异常处理
    ├── middleware              中间件
    │   └── __init__.py
    │   └── log.py             log处理中间件
    ├── response.py             统一返回封装
    └── tools                   常用工具
        ├── __init__.py
        ├── apollo_client.py    apollo相关操作
        ├── bitmap.py           位图相关操作
        ├── config.py           配置载入相关操作
        ├── dot_dict.py         提供字典的dot访问模式
        ├── fields.py           数据库fields相关操作
        ├── paginator.py        分页相关相关操作
        └── redis.py            redis相关操作

14 directories, 38 files

```



## 项目启动

### 初始化数据库

    1. 找到 models/migrate.py 文件，修改默认管理员账号秘密
    2. python 执行 models/migrate.py 文件

### 本地

    1. 执行 echo "from .base import *" > conf/config/local.py
    2. 添加你的配置到 conf/config/local.py 中

### 测试环境

    1. 执行 echo "from .base import *" > conf/config/test.py 
    2. 添加你的配置到 conf/config/test.py 中
    2. 执行 echo "CONF_MODULE=dev" > .env
    3. docker-compose build 
    4. docker-compose up -d 

### OpenAPI 地址

    1. http://0.0.0.0:8000/docs

### Redoc 地址

    1. http://0.0.0.0:8000/redoc
