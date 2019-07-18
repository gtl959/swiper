from django.urls import path
from user.apis import *

urlpatterns = [
    path('verify/',verify_phone_num),
    path('login/',login),
    path('get_profile/',get_profile),
    path('set_profile/',set_profile),
    path('upload_avatar/',upload_avatar),
]