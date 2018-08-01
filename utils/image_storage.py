# coding:utf-8

from qiniu import Auth, put_file, etag, put_data
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'tvZGOWCU4tQGA6fVeJdrMlsXcECWrm_XK2KaD0u1'
secret_key = 'Sg7t7V9GX4_HIbO2WFsf6M0E1dd1dZbxS8iAURT7'


def storage(image_data):
    if not image_data:
        return None
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'ihome'
    # 上传到七牛后保存的文件名
    # key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    ret, info = put_data(token, None, image_data)
    print(info)
    return ret['key']