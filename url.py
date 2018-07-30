# coding:utf-8
from handlers import Passport,VerifvCode

handlers = [
    (r"/",Passport.IndexHandler),
    (r"/api/imagecode",VerifvCode.ImageCodeHandler),

]