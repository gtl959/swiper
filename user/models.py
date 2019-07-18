from datetime import datetime, date

from django.db import models

# Create your models here.
from libs.orm import ModelToDictMixin

SEXS = (
    ('0', '未知'),
    ('1', '男'),
    ('2', '女'),
)

LOCATIONS = (
    ('gz', '广州'),
    ('bj', '北京'),
    ('sz', '深圳'),
    ('sh', '上海'),
)

IS_OR_NOT = (
    ('0','否'),
    ('1','是')
)


class User(models.Model,ModelToDictMixin):


    phoneNum = models.CharField(max_length=11,unique=True)
    nickNum = models.CharField(max_length=100)
    sex = models.CharField(max_length=2,default='0',choices=SEXS)
    birth_year = models.IntegerField(default=1999)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=36,choices=LOCATIONS)

    class Meta:
        db_table = "user"

    #求出年龄
    @property
    def age(self):
        now = date.today()
        birthday = date(self.birth_year,self.birth_month,self.birth_day)
        delta = (now - birthday).days // 365 - 1     #先用求出年龄相差的天数整除365天减去1天
        if now.month > birthday.month:
           return delta
        else:
            if now.month == birthday.month and now.day > birthday.day:
                return delta
            else:
                return delta + 1

    def to_dict(self,exclude=None):
        dic = super(User, self).to_dict()
        dic['age'] = self.age
        return dic

    @property
    def profile(self):
        if not hasattr(self,'_profile'):
            self._profile , _ = Profiles.objects.get_or_create(id=self.id)
        return self._profile


















class Profiles(models.Model,ModelToDictMixin):
    location = models.CharField(max_length=36,choices=LOCATIONS,default='gz')
    min_distance = models.IntegerField(default=0)
    max_distance = models.IntegerField(default=5)
    min_dating_age = models.IntegerField(default=18)
    max_dating_age = models.IntegerField(default=81)
    dating_sex = models.CharField(max_length=2,default='0',choices=SEXS)
    auto_play = models.CharField(max_length=2,default='0',choices=IS_OR_NOT)



    class Meta:
        db_table='profiles'



