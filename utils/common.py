# coding:utf-8
from utils.response_code import RET
import functools

def require_logined(func):
    @functools.wraps(func)
    def inner(request_handler_obj,*args,**kwargs):
        # 根据get_current_user()方法进行判断，如果返回的不是一个空字典，证明用户已经登陆过，保存了用户session数据。
        if request_handler_obj.get_current_user():
            func(request_handler_obj,*args,**kwargs)
        else:
            request_handler_obj.write(dict(errno=RET.SESSIONERR,errmsg="用户未登陆"))
    return inner