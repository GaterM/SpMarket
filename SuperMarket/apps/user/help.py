import hashlib
from django.conf import settings


# 密码加密
from django.shortcuts import redirect
from django.urls import reverse


def set_password(pwd):
    token = settings.SECRET_KEY
    password = token + pwd
    h = hashlib.sha1(password.encode('utf-8'))
    return h.hexdigest()


# 登录验证装饰器
def verify_login_required(fun):
    def verify_login(request, *args, **kwargs):
        rs = request.session.get("ID")
        if rs is None:
            return redirect(reverse('user:login'))
        else:
            return fun(request, *args, **kwargs)
    return verify_login