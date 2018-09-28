from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseView
from goods.models import Goods_sku


# 保存购车车在 redis 中
# 商品的添加
class SaveShopCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 验证是否登录, 并保存用户 id
        user_id = request.session.get('ID')
        if user_id is None:
            return JsonResponse({"error": 1, "msg": "用户未登录,请登录!"})
        user_id = user_id
        # 获取商品id
        sku_id = request.POST.get('sku_id')
        # 获取货物数量
        goods_count = request.POST.get('goods_count')
        # 验证数据合法性
        try:
            sku_id = int(sku_id)
            goods_count = int(goods_count)
        except Exception as e:
            return JsonResponse({"error": 2, "msg": "数据不合法"})
        # 验证商品是否存在
        try:
            good = Goods_sku.objects.get(pk=sku_id)
        except Exception as e:
            return JsonResponse({"error": 3, "msg": "商品已下架,请重新选择商品!"})
        #  验证库存是否足够
        good = Goods_sku.objects.get(pk=sku_id)
        stock = good.Stock
        if goods_count > stock:
            return JsonResponse({"error": 4, "msg": "商品库存不足"})
        # 连接 redis 保存数据到 redis 中
        cnn = get_redis_connection("default")
        # 保存到redis对象hash中,设置hash的key
        car_key = "car_%s" % (user_id)  # 当前用户的购物车键
        #  保存购物车
        cnn.hincrby(car_key, sku_id, goods_count)
        # 计算购物车数量
        car_total = 0
        vals = cnn.hvals(car_key)
        if len(vals) > 0:
            for val in vals:
                car_total += int(val)
        return JsonResponse({"error": 0, "msg": "商品添加成功", "car_total": car_total})


# 删除购物车
class DelShopCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 验证是否登录, 并保存用户 id
        user_id = request.session.get('ID')
        if user_id is None:
            return JsonResponse({"error": 1, "msg": "用户未登录,请登录!"})
        user_id = user_id
        # 获取商品id
        sku_id = request.POST.get('sku_id')
        # 获取货物数量
        # goods_count = request.POST.get('goods_count')
        # 验证数据合法性
        try:
            sku_id = int(sku_id)
            # goods_count = int(goods_count)
        except Exception as e:
            return JsonResponse({"error": 2, "msg": "数据不合法"})
        # 验证商品是否存在
        try:
            good = Goods_sku.objects.get(pk=sku_id)
        except Exception as e:
            return JsonResponse({"error": 3, "msg": "商品不存在!"})
        # 连接 redis 保存数据到 redis 中
        cnn = get_redis_connection("default")
        # 保存到redis对象hash中,设置hash的key
        car_key = "car_%s" % (user_id)  # 当前用户的购物车键
        # 判断对应商品购物车数量是否大于0
        good_count = cnn.hget(car_key, sku_id)
        if int(good_count) > 0:
            cnn.hincrby(car_key, sku_id, -1)
        else:
            cnn.hdel(car_key, sku_id)
        # 获取用户购物车总数量
        car_total = 0
        vals = cnn.hvals(car_key)
        if len(vals) > 0:
            for val in vals:
                car_total += int(val)
        return JsonResponse({"error": 0, "msg": "商品删除成功", "car_total": car_total})


# 购物车显示数量
class ShowShopCarView(BaseView):
    def get(self, request):
        # 总价格
        total_price = 0
        # 总数量
        total_count = 0
        # 从redis获取商品展示
        user_id = request.session.get('ID')
        car_key = "car_%s" % (user_id)  # 当前用户的购物车键
        cnn = get_redis_connection('default')
        goods_car = cnn.hgetall(car_key)
        # print(goods)
        goods = []
        for sku_id, goods_count in goods_car.items():
            sku_id = int(sku_id)
            goods_count = int(goods_count)
            good = Goods_sku.objects.get(pk=sku_id)
            # 获取总价格
            total_price += good.goods_price * goods_count
            total_count += goods_count
            # 在商品对象上新增一个数量属性
            good.goods_count = goods_count
            goods.append(good)
        context = {
            "goods": goods,
            "total_price": total_price,
            "total_count": total_count,
        }
        return render(request, 'shopcar/shopcart.html', context)


    def post(self, request):
        pass
