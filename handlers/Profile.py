# coding:utf-8

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.image_storage import storage
import logging
import config

class AvatarHandler(BaseHandler):
    """上传图片"""
    @require_logined
    def post(self):
        try:
            image_data = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.error(e)
            return self.write()
        try:
            key = storage(image_data)
        except Exception as e:
            logging.error(e)
            return self.write()
        try:
            self.db.execute("update")
        except Exception as e:
            logging.error(e)
            return self.write()
        image_url = config.image_url_prefix + key
        return image_url
