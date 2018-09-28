from django.conf.urls import url

from shopcar.views import SaveShopCarView, DelShopCarView, ShowShopCarView

urlpatterns = [
    url(r'^saveshopcar/$', SaveShopCarView.as_view(), name='saveshopcar'),
    url(r'^delshopcar/$', DelShopCarView.as_view(), name='delshopcar'),
    url(r'^showshopcar/$', ShowShopCarView.as_view(), name='showshopcar'),
]