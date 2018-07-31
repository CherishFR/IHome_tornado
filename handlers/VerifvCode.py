# coding:utf-8

from .BaseHandler import BaseHandler
from utils.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp

import logging
import constants
import random

class ImageCodeHandler(BaseHandler):
    """生成验证码"""
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s" % pre_code_id)
            except Exception as e:
                logging.error(e)
        # name 图片验证码名称
        # text 图片验证码文本
        # image 图片验证码二进制数据
        name,text,image = captcha.captcha.generate_captcha()
        try:
            self.redis.setex("image_code_%s" % code_id, constants.PIC_CODE_EXPIRES_SECONDS,text)
        except Exception as e:
            logging.error(e)
            self.write("")
        self.set_header('Content-Type','image/jpg')
        self.write(image)

class PhoneCodeHandler(BaseHandler):
    """验证图片验证码，并发送手机验证码"""
    def post(self):
        mobile = self.json_args.get("mobile")
        image_code_id = self.json_args.get("image_code_id")
        image_code_text = self.json_args.get("image_code_text")
        if not all((mobile,image_code_id,image_code_text)):
            return self.write(dict(errno=RET.PARAMERR,errmsg="参数不完整"))
        try:
            real_image_code_text = self.redis.get("image_code_%s" % image_code_id)
        except Exception as e :
            logging.error(e)
            return self.write(dict(errno=RET.DBERR,errmsg="查询出错"))
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="图片验证码过期"))
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码输入错误"))
        sms_code = "%04d" % random.randint(0,9999)  # 生成短信验证码
        try:
            self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS,sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="生成短信验证码错误"))
        try:
            ccp.sendTemplateSMS(mobile,[sms_code,constants.SMS_CODE_EXPIRES_SECONDS/60],1)
        except  Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送短信验证码失败"))
        self.write(dict(errno=RET.OK,errmsg="OK"))

