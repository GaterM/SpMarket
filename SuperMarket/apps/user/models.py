from django.core import validators
from django.db import models
from db.base_model import BaseModel


# Create your models here.


# 创建登录注册模型
class Reg_login(BaseModel):
    sex_choices = (
        (1, '男'),
        (2, "女"),
        (3, '保密'),
    )
    tel = models.CharField(max_length=11, verbose_name='手机号码', validators=[
        validators.RegexValidator(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', '手机号码格式错误')
    ])
    password = models.CharField(max_length=64, verbose_name='登录密码')
    born = models.DateField(verbose_name='出生日期', null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    sex = models.SmallIntegerField(choices=sex_choices, default=3, verbose_name='性别')
    school = models.CharField(max_length=20, null=True, blank=True, verbose_name='学校名字')
    hometown = models.CharField(max_length=200, null=True, blank=True, verbose_name='家乡')
    head = models.ImageField(verbose_name='用户头像', upload_to='user/%Y%m/%d', default='image/shop3.png')
    address = models.CharField(verbose_name='详细地址', max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'reg-login'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


# 创建收货地址模型
class Address(BaseModel):
    username = models.ForeignKey(to='Reg_login', verbose_name='用户名')
    consignee = models.CharField(max_length=20, verbose_name='收货人')
    tel = models.CharField(max_length=11, verbose_name='收货人电话')
    province = models.CharField(max_length=20, verbose_name='省')
    city = models.CharField(max_length=20, verbose_name='市')
    county = models.CharField(max_length=20, verbose_name='县')
    street = models.CharField(max_length=50, verbose_name='街道')
    detail_addr = models.CharField(max_length=100,verbose_name='详细地址')
    pass
