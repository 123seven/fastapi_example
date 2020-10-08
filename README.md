## 项目说明

 FastApi Restful Api 项目示例


## 项目技术栈

**Fastapi:**  用于web服务构建  
**Tortoise-orm:** Python异步ORM  
**Orjson:** 最快的Python Json库  
**Uvicorn:** 基于 asyncio 开发的一个轻量级高效的 Web 服务器框架  
**Pydantic:** Python类型提示以及进行数据验证和设置管理  
**Bcrypt:** 用户信息加密  
**docker:** 服务环境构建  
**docker-compose:** 服务环境快速构建  

#### 自写模块
**AutoModelSerializer:** 用于序列化/自定义返回数据，现Python中最快  
**Config:** 多环境配置读取  
**Response:** RESTful 返回统一数据格式  



## 项目结构

```
.
├── Dockerfile             docker file部署文件
├── README.md
├── apps                   app目录
│   ├── __init__.py        app 启动入口
│   ├── admin              管理后台接口
│   │   ├── __init__.py
│   │   └── admin.py
│   └── api                一般API接口
│       ├── __init__.py
│       └── v1             版本区分 
│           └── __init__.py
├── conf                   配置文件目录
│   ├── __init__.py
│   └── config            
│       ├── __init__.py
│       ├── base.py       基础配置文件
│       ├── dev.py        dev环境配置
│       └── local.py      本地环境配置
├── deploy                部署依赖等
│   ├── pip.conf          pip豆瓣源，加速安装速度
│   ├── sources.list
├── docker-compose.yml    docker-compose 文件
├── main.py               程序入口
├── models                数据库model
│   ├── __init__.py
│   ├── admin.py
│   └── migrate.py        migrate文件，修改model后需要手动执行migrate文件
├── requirements.txt      项目python依赖
├── schemas               open API schemas
│   ├── __init__.py
│   └── admin.py
├── tests                 测试用例
│   └── __init__.py
└── utils                 工具包
    ├── __init__.py
    ├── authentication.py token相关
    ├── config.py         配置读取
    ├── paginator.py      分页
    ├── response.py       返回定制
    └── serializers.py    数据序列化

11 directories, 29 files
```



## 项目启动

### Local

    1. echo "from .base import *" > conf/config/local.py
    2. add your configuration save to conf/config/local.py

### Deployment

    1. add your configuration save to /conf/config/dev.py
    2. echo "CONF_MODULE=dev" > .env
    3. docker-compose build 
    4. docker-compose up -d 



## 项目更新

### Update

    1. sh update.sh
    
## 初始化数据库
    找到 `models/migrate.py` 文件，修改默认管理员账号秘密，再执行即可。