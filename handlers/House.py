# coding:utf-8

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined
import constants
import logging
import json



class AreaInfoHandler(BaseHandler):
    """区域选择"""
    def get(self):
        try:
            ret = self.redis.get("area_info")  # 拿到的数据为json格式
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            logging.debug(ret)
            logging.info("hit redis")
            return self.write('{"errno":%s,"errmsg":"ok","data":%s}' %(RET.OK,ret))
        try:
            ret = self.db.query("select ai_area_id,ai_name from ih_area_info")
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR,errmsg="get user error"))
        if not ret:
            return self.write(dict(errno=RET.NODATA, errmsg="no area data"))
        areas = []
        for i in ret:
            area = {"area_id":i["ai_area_id"],"name":l["ai_name"]}
            areas.append(area)
        try:
            self.redis.setex("area_info",constants.REDIS_AREA_INFO_EXPIRES_SECONDES,json.dumps(areas))
        except Exception as e:
            logging.error(e)
        self.write(dict(errno=RET.OK,errmsg="ok",data=areas))


class MyHousesHandler(BaseHandler):
    """"""
    @require_logined
    def get(self):
        user_id = self.session.data["user_id"]
        try:
            ret = self.db.query("select a.hi_house_id,a.hi_title,a.hi_price,a.hi_ctime,b.ai_name,a.hi_index_image_url " \
                  "from ih_house_info a inner join ih_area_info b on a.hi_area_id=b.ai_area_id where hi_user_id=%(user_id)s",user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno= RET.DBERR, errmsg="get data error"))
        houses = []
        if ret:
            for i in ret:
                house = {
                    "house_id": i["hi_house_id"],
                    "title": i["hi_title"],
                    "price": i["hi_price"],
                    "ctime": i["hi_ctime"].strftime("%Y-%m-%d"),  # 将返回的Datatime类型格式化为字符串
                    "area_name": i["ai_name"],
                    "img_url": constants.QINIU_URL_PREFIX + i["hi_index_image_url"] if i["hi_index_image_url"] else ""
                }
                houses.append(house)
        self.write(dict(errno= RET.OK, errmsg="OK", houses=houses))