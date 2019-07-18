import os
from urllib.parse import urljoin

from django.core.cache import cache

from common.utils import verify_random_code, upload_picture
from libs.qiniuyun import upload
from libs.sms import send_verify_code
from common import config

from worker import celery_app

#是否验证码发送成功
from swiper.settings import UPLOADS_ADDR


def is_send_verify_code(phone_num):

    #生成验证码
    code = verify_random_code(4)
    #发送验证码,返回是否发送成功
    res = send_verify_code(phone_num,code)
    if res:
        cache.set(config.USER_VERIFY_CODE.format(phone_num),code,300)

    return res


def upload_avatar_to_qcy(file_addr,file_name):


    #上传文件到云端
    ret,info = upload(file_name,file_addr)

    return True if info.status_code == 200 else False


#
@celery_app.task
def celery_upload_to_qcy(file,file_name,user):

    # 本地存储地址
    file_addr = os.path.join(UPLOADS_ADDR , file_name)

    # 上传文件到本地存储地址
    if upload_picture(file_addr, file):
        #上传本地成功后上传到云端
        ret = upload_avatar_to_qcy(file_addr,file_name)
        #上传云端成功后保存到user对象身上
        if ret:
            user.avatar = urljoin(config.QNY_HOST,file_name)
            user.save()

