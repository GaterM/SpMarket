from django.conf.urls import url

from goods.views import IndexView, CategoryView, GoodsDetailView

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<cate_id>\d+)_(?P<order>\d)/$', CategoryView.as_view(), name='category'),
    url(r'^detail/(?P<sku_id>\d+)/$',GoodsDetailView.as_view(), name='detail'),
]
