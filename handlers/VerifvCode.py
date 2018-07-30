# coding:utf-8

from .BaseHandler import BaseHandler
from utils.captcha import captcha

import logging
import constants

class ImageCodeHandler(BaseHandler):
    """"""
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete("")
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

