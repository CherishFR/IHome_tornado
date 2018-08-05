# coding:utf-8
from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import require_logined
import logging
import re
import hashlib
import config


class RegisterHandler(BaseHandler):
    """电话验证以及注册"""
    def post(self):
        mobile = self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        passwd = self.json_args.get("password")
        if not all((mobile,sms_code,passwd)):
            return self.write(dict(errno=RET.PARAMERR, errmsg='参数不完整'))
        if not re.match(r'1\d{10}$',mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg='电话格式不正确'))
        try:
            redis_sms_code = self.redis.get("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='查询出错'))
        if not redis_sms_code:
            return self.write(dict(errno=RET.NODATA, errmsg='电话验证码已失效'))
        if redis_sms_code != sms_code:
            return self.write(dict(errno=RET.PARAMERR, errmsg='电话验证码输入错误'))
        try:
            self.redis.delete("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)
        # 注册
        pwd = hashlib.sha256(passwd+config.passwd_hash_key).hexdigest()
        sql = "insert into ih_user_profile(up_name,up_mobile,up_passwd) values (%(name)s,%(mobile)s,%(passwd)s)"
        try:
            user_id = self.db.execute(sql,name=mobile,mobile=mobile,passwd=pwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAEXIST, errmsg="手机号已存在"))
        # 将用户信息保存在session中
        session = Session(self)
        session.data["user_id"] = user_id
        session.data["mobile"] = mobile
        session.data["name"] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)
        self.write(dict(errno=RET.OK, errmsg="注册成功"))


class LoginHandler(BaseHandler):
    """登录"""
    def post(self):
        mobile = self.json_args.get("mobile")
        passwd = self.json_args.get("password")
        if not all((mobile,passwd)):
            return self.write(dict(errno=RET.PARAMERR, errmsg='参数不完整'))
        if not re.match(r'1\d{10}$',mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg='电话格式不正确'))
        try:
            res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s",mobile=mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="没有注册该账号"))
        pwd = hashlib.sha256(passwd+config.passwd_hash_key).hexdigest()
        if unicode(pwd) != res["up_passwd"]:
            try:
                self.session = Session(self)
                self.session.data["user_id"] = res["up_user_id"]
                self.session.data["mobile"] = mobile
                self.session.data["name"] = res["up_name"]
                self.session.save()
            except Exception as e:
                logging.error(e)
            else:
                return self.write(dict(errno=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errno=RET.DATAERR, errmsg="手机号或密码错误"))



class CheckLoginHandler(BaseHandler):
    """登陆状态检测"""
    def get(self):
        if self.get_current_user():
            self.write(dict(errno=RET.OK, errmsg="true", data={"name":self.session.data.get("name")}))
        else:
            self.write(dict(errno=RET.NODATA, errmsg="没有用户信息"))

class LogoutHandler(BaseHandler):
    """退出登录"""
    @require_logined
    def get(self):
        # 清除session数据
        # sesssion = Session(self)
        self.session.clear()
        self.write(dict(errno=RET.OK, errmsg="退出成功"))