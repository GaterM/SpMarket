from django.db import models

# Create your models here.

# 创建登录注册模型
class Res_login(models.Model):
    tel = models.CharField(max_length=11, verbose_name='手机号码')
    password = models.CharField(max_length=100, verbose_name='登录密码')

    class Meta:
        db_table = 'res-login'
