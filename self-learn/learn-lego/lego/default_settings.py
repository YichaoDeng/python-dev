import os
import sys

BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)

CONCURRENCY = 1

# web socket 服务端地址
WEB_SOCKET_SERVER = "http://localhost:8000"
# web socket 通信地址
WEB_SOCKET_CONNECT_PATH = "/ws/{app_id}"

# 主从模式
MODE_SERVER_TO_CLIENT_OR_TASK = 0
MODE_SERVER_TO_CLIENT_TO_TASK = 1
MASTER_SLAVE_MODE = MODE_SERVER_TO_CLIENT_OR_TASK
WHITE_LIST = []

# API 事件监听
EVENTS = {
    "exception": [],
    "request": [],
    "response": [],
    "startup": [],
    "shutdown": [],
}

# APS Scheduler 配置
SHCHEDULE_CONFIG = {}

# celery worker
CELERY_WORKER = {}

# 安全相关配置 -> 账号密码
SECURITY_CONFIG = {}

# 注册的 apps
APPS = []
# 注册的 views
VIEWS = []
