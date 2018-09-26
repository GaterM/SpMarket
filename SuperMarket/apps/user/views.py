import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from db.base_view import BaseView
from user.forms import LoginModelForm, RegisterModelForm, InfoModelForm
from user.help import send_sms
from user.models import Reg_login


# 创建登录
class LoginView(View):
    def get(self, request):
        form = LoginModelForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginModelForm(request.POST)
        if form.is_valid():
            # 验证成功,保存登录标识到session中
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['tel'] = user.tel
            request.session.set_expiry(0)
            # 跳转到个人中心
            return redirect(reverse('user:center'))
        # 验证失败
        return render(request, 'user/login.html', {'form': form})


# 创建注册
class RegisterView(View):
    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'user/reg.html', {'form': form})

    def post(self, request):
        verify_code_session = request.session.get('verify_code_session')
        data = request.POST.dict()
        data['verify_code_session'] = verify_code_session
        form = RegisterModelForm(data)
        # 注册成功
        if form.is_valid():
            form.save()
            return redirect(reverse('user:login'))
        # 注册失败
        return render(request, 'user/reg.html', {'form': form})


# 创建收货地址
class AddressView(BaseView):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'user/address.html')


# 创建个人中心
class CenterView(BaseView):
    def get(self, request):
        tel = request.session.get('tel')
        return render(request, 'user/member.html', {'tel': tel})

    def post(self, request):
        pass


# 创建个人资料
class InfoView(BaseView):
    def get(self, request):
        tel = request.session.get('tel')
        return render(request, 'user/infor.html', {'tel': tel})

    def post(self, request):
        form = InfoModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user/reg.html', {'form': form})
            # 注册失败
        return render(request, 'user/reg.html', {'form': form})


@csrf_exempt  # 移除令牌限制
def upload_head(request):
    if request.method == 'POST':
        # 获取用户id
        user_id = request.session.get('ID')
        # 获取用户对象
        user = Reg_login.objects.get(pk=user_id)
        user_head =request.FILES['file']  # 获取对应文件
        user.save()
        return JsonResponse({"error":0})
    else:
        return JsonResponse({"error":1})



# 创建退出
class LogoutView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


# 发送验证码
class SendCodeView(View):
    def post(self, request):
        # 获取数据
        tel = request.POST.get('tel', '')
        # 处理数据
        import re
        # 匹配手机号码是否符合正则
        tel_re = re.compile(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        rs = re.search(tel_re, tel)
        if rs is None:
            # 手机格式错误
            return JsonResponse({"status": 400, "msg": '手机号码格式错误'})
        # 验证手机号码是否注册
        user = Reg_login.objects.filter(tel=tel_re).exists()
        if user:
            return JsonResponse({"status": 400, "msg": '手机号码已经注册'})

        # 生成验证码
        import random
        verify_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # print(verify_code)
        # 发送验证码
        print("====={}======".format(verify_code))
        # 发送短信   用阿里云
        __business_id = uuid.uuid1()
        # print(__business_id)
        params = "{\"code\":\"%s\"}" % verify_code
        rs = send_sms(__business_id, tel, "LitterSpider", "SMS_145599624", params)
        print(rs)
        # 保存验证码到session中
        request.session['verify_code_session'] = verify_code
        request.session.set_expiry(0)
        return JsonResponse({"status": 200})
