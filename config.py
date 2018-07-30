# coding:utf_8
import os

# Application配置参数
setting = {
    "static_path": os.path.join(os.path.dirname(__file__), "statics"),
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "cookie_secret":"rrqUEK3hSgCnknxltqspZXTS2Yu0LEsXr3anyxzG1Mo=",
    "xsrf_cookies":True,
    "debug":True,
}

# mysql
mysql_options = dict(
    host='127.0.0.1',
    database="ihome",
    user='liu',
    password = "Jm25csdb."
)

# redis
redis_options = dict(
    host='127.0.0.1',
    port=6379
)

# log
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"
