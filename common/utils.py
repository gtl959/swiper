import re
import random
import hashlib
import time

rc = re.compile(r'^1[3-9]\d{9}$')

def judge_phone_num(phone_num):

    if rc.match(phone_num):
        return True
    else:
        return False

def verify_random_code(num=4):

    if num < 1 or not isinstance(num,int):
        num = 1
    code = random.randrange(10 ** (num-1),10 ** num)
    return str(code)

def calc_md5(passwd):
    md5 = hashlib.md5()
    md5.update(passwd.encode('utf-8'))
    return md5.hexdigest()

#生成token
def create_token():
    return calc_md5(str(time.time())+str(random.random()))

#上传图片文件
def upload_picture(file_addr,file):
    try :
        with open(file_addr,'wb+') as f :
            for i in file.chunks():
                f.write(i)
        return True
    except Exception as e :
        return False