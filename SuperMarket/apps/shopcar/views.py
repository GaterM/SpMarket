from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from goods.models import Goods_sku


class SaveShopCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 获取商品id
        sku_id = request.POST.get('sku_id')
        # 获取货物数量
        goods_count = request.POST.get('goods_count')
        # 验证是否登录
        user_id = request.session.get('ID')
        if user_id is None:
            return JsonResponse({"error":1, "msg":"用户未登录,请登录!"})
        user_id = user_id
        # 验证数据合法性
        try:
            sku_id = int(sku_id)
            goods_count = int(goods_count)
        except Exception as e:
            return JsonResponse({"error":2, "msg":"数据不合法"})
        # 验证商品是否存在
        try:
            good = Goods_sku.objects.get(pk=sku_id)
        except Exception as e:
            return JsonResponse({"error":3, "msg":"商品已下架,请重新选择商品!"})
        #  验证库存是否足够
        good = Goods_sku.objects.get(pk=sku_id)
        stock = good.Stock
        if goods_count > stock:
            return JsonResponse({"error":4, "msg":"商品库存不足"})
        # 连接 redis 保存数据到 redis 中
        cnn = get_redis_connection("default")
        # 保存到redis对象hash中,设置hash的key
        car_key = "car_%s"%(user_id) # 当前用户的购物车键
        #  保存购物车
        cnn.hincrby(car_key, sku_id, goods_count)

        car_total
