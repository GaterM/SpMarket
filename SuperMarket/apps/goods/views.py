from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# 商品首页
from django_redis import get_redis_connection

from goods.models import Goods_sku, Broadcast, Activity, Goods_category, Activity_area


class IndexView(View):
    def get(self, request):
        broadcast = Broadcast.objects.all().order_by('-create_time')[:2]
        activity = Activity.objects.all().order_by('-id')[:5]
        areas = Activity_area.objects.filter(is_delete=False)
        # goods = areas.activity_goods_set
        context = {
            "broadcast": broadcast,
            "activity": activity,
            "areas": areas,
        }
        return render(request, 'goods/index.html', context)

    def post(self, request):
        pass


# 商品分类
class CategoryView(View):
    def get(self, request, cate_id=0, order = 0):
        # 获取分类id
        cate_id = int(cate_id)
        # 获取所有的分类
        categorys = Goods_category.objects.filter(is_delete=False)
        if cate_id == 0:
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据传入id 查询对应id的分类
            category = Goods_category.objects.get(pk = cate_id)
        # 根据分类查询商品
        # goods_sku = Goods_sku.objects.filter(is_delete=False)
        # 根据点击排序
        order_by_rule = ['id', 'sales_volume', '-goods_price', 'goods_price', '-create_time']
        order = int(order)
        goods_sku = category.goods_sku_set.all().order_by(order_by_rule[order])
        # 获取用户id
        car_total = 0
        user_id = request.session.get("ID")
        if user_id:
            # 链接redis
            cnn = get_redis_connection("default")
            car_key = "car_%s" % (user_id)
            vals = cnn.hvals(car_key)
            if len(vals) > 0:
                for val in vals:
                    car_total += int(val)

        context = {
            "goods_sku": goods_sku,
            "cate_id": cate_id,
            "categorys": categorys,
            "order": order,
            "car_total":car_total,
        }
        return render(request, 'goods/category.html', context)

    def post(self, request):
        pass


# 商品详情
class GoodsDetailView(View):
    def get(self, request, sku_id):
        try:
            sku_id = int(sku_id)
            good = Goods_sku.objects.get(pk=sku_id)
            return render(request, 'goods/detail.html', {"good": good})
        except:
            return redirect(reverse("goods:index"))

    def post(self, request):
        pass

# class ActivityView(View):
#     def get(self, request):
#
#         return render(request, 'goods/index.html',)
