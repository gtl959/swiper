# -*- coding: utf-8 -*-
# flake8: noqa
from common import config
from qiniu import Auth, put_file, etag
import qiniu.config

def upload(file_name,file_path):
    #需要填写你的 Access Key 和 Secret Key
    access_key = config.QNY_ACCESS_KEY
    secret_key = config.QNY_SECRET_KEY
    #构建鉴权对象
    q = Auth(access_key,secret_key)
    #要上传的空间
    bucket_name = config.QNY_BUCKET_NAME
    #上传后保存的文件名
    key = file_name
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = file_path

    ret, info = put_file(token, key, localfile)
    # print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)
    return ret, info


