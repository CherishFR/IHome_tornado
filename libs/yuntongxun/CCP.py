# coding:utf-8

from CCPRestSDK import REST
import ConfigParser
import logging

#主帐号
accountSid= '8aaf070864ef775a0164efd30ffe0034'

#主帐号Token
accountToken= '93ca99e553fd4e4c854a22d90179ee3c'

#应用Id
appId='8aaf070864ef775a0164efd3105a003a'

#请求地址，格式如下，不需要写http://
serverIP='sandboxapp.cloopen.com'

#请求端口
serverPort='8883'

#REST版本号
softVersion='2013-12-26'
class CCP(object):
    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @classmethod
    def instance(cls):
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)

ccp = CCP.instance()

if __name__ == "__main__":
    ccp.sendTemplateSMS("18516952650", ["1234", 5], 1)
