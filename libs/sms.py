import requests
from common.config import YZX_SMS_PARAMS, YZX_SMS_URL
from swiper.settings import DEBUG


def send_verify_code(phone_num, code):
    if DEBUG:
        print(phone_num, code)
        return True
    req = requests.post(YZX_SMS_URL, json=YZX_SMS_PARAMS)
