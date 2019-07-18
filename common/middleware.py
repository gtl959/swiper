from django.utils.deprecation import MiddlewareMixin

from common.errors import LOGIN_STATUS_ERROR
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    '''
        #通过session校验用户是否登录状态的中间件
    '''

    def process_request(self,request):

        # 设置校验登录状态的白名单
        WHITE_APIS = [
            '/api/user/verify/',
            '/api/user/login/'
        ]
        print(request.path)
        #如果是白名单接口，则不用判断是否已登录
        if request.path in WHITE_APIS:
            return                     #直接return就是跳过

        #查出session有没有uid，有就是登录，没就是没登录或者登录失效
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=LOGIN_STATUS_ERROR)

        #把user整个对象（用户信息）绑定在request对象身上
        request.user = User.objects.get(id=uid)



        #一般都是使用token
        #HTTP_这个是固定前缀，而LOGIN_TOKEN可以随意，根据传去前端是什么参数名字
        #token = request.META.get('HTTP_LOGIN_TOKEN')
        #if not token:
        #   return render_json(code=LOGIN_STATUS_ERROR)





