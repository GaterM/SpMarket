from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from db.base_view import BaseView
from user.forms import LoginModelForm, RegisterModelForm, InfoModelForm
from user.models import Reg_login

# 创建登录
class LoginView(View):
    def get(self, request):
        form = LoginModelForm()
        return render(request, 'user/login.html', {'form':form})

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
        return render(request, 'user/login.html', {'form':form})
# 创建注册
class RegisterView(View):
    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'user/reg.html', {'form': form})

    def post(self, request):
        form = RegisterModelForm(request.POST)
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
        return render(request, 'user/member.html', {'tel':tel})

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


# 创建退出
class LogoutView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
