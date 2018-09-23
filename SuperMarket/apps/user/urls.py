from django.conf.urls import url

from user.views import LoginView, RegisterView, CenterView, InfoView, LogoutView, AddressView, SendCodeView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    url(r'^register/$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^center/$', CenterView.as_view(), name='center'),  # 个人中心
    url(r'^info/$', InfoView.as_view(), name='info'),  # 个人资料
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  # 退出
    url(r'^address/$', AddressView.as_view(), name='address'),  # 收货地址
    url(r'^send/$', SendCodeView.as_view(), name='send'),  # 验证码
]