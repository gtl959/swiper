from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from common import errors
from common.config import USER_VERIFY_CODE
from common.errors import VERIFY_CODE_ERROR, FORM_DATA_ERROR, UPLOAD_PICTURE_ERROR
from common.utils import judge_phone_num, create_token, upload_picture
from libs.http import render_json
from swiper.settings import UPLOADS_ADDR
from user.forms import ProfileForm
from user.logics import is_send_verify_code, upload_avatar_to_qcy, celery_upload_to_qcy
from user.models import User


def verify_phone_num(request):
    '''
    判断用户手机格式是否正确以及给用户发送验证码
    :param request:
    :return:
    '''
    phone_num = request.POST.get('phone_num')

    if judge_phone_num(phone_num):
        if is_send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SEND_VERIFY_CODE_ERROR)
    else:
        return render_json(code=errors.PHONE_NUM_ERROR)


def login(request):
    '''
        登录或者注册接口
    :param request:
    :return:
    '''
    phone_num = request.POST.get('phone_num','').strip()
    verify_code = request.POST.get('verify_code','').strip()

    cache_verify_code = cache.get(USER_VERIFY_CODE.format(phone_num))

    #校验验证码
    if verify_code != cache_verify_code:
        return render_json(code=VERIFY_CODE_ERROR)

    #获取或者创建用户信息
    user,created = User.objects.get_or_create(phoneNum=phone_num)

    #在session设置登录状态
    request.session['uid'] = user.id

    return render_json(data=user.to_dict())


def get_profile(request):
    '''
    获取个人求偶信息
    :param request:
    :return:
    '''
    return render_json(data=request.user.profile.to_dict(exclude=['auto_play']))

def set_profile(request):
    '''
    设置个人求偶信息
    :param request:
    :return:
    '''
    user = request.user

    # data 存表单提交过来都所有数据， instance是一个profile实例
    form = ProfileForm(data=request.POST,instance=user.profile)


    if form.is_valid():
        form.save()
        return render_json()
    else:
        return render_json(code=FORM_DATA_ERROR,data=form.errors)


def upload_avatar(request):
    '''
    上传用户图片
    :param request:
    :return:
    '''
    user = request.user

    avatar = request.FILES.get('avatar')
    avatar_name = 'avatar_{}'.format(create_token())

    # 上传到本地的方法
    # avatar_addr = UPLOADS_ADDR + '/avatar/' +avatar_name
    # #上传图片
    # if upload_picture(avatar_addr,avatar):
    #
    #     user.avatar = avatar_addr
    #     user.save()
    #     return render_json()
    # else:
    #     return render_json(code=UPLOAD_PICTURE_ERROR)

    # 上传到云端的方法
    celery_upload_to_qcy.delay(avatar,avatar_name,user)

    return render_json()








