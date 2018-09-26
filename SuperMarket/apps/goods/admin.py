from django.contrib import admin
from goods.models import Goods_category, Goods_unit, Goods_spu, Goods_album, Goods_sku, Broadcast, Activity_goods, \
    Activity_area, Activity

admin.site.site_header = '商城管理'

@admin.register(Goods_category)
class Goods_categoryAdmin(admin.ModelAdmin):
    # 商品分类
    pass

@admin.register(Goods_unit)
class Goods_unitAdmin(admin.ModelAdmin):
    # 商品单位
    pass


@admin.register(Goods_spu)
class Goods_spuAdmin(admin.ModelAdmin):
    # 商品SPU
    pass


# 关联商品的相册
class Goods_skuAdminInLine(admin.TabularInline):
    model = Goods_album
    extra = 3
    fields = ['image_addr', 'goods_sku']


# 注册GoodsSKU的模型到后台
@admin.register(Goods_sku)
# 定制显示效果
class GoodsSKUAdmin(admin.ModelAdmin):
    # 商品SPU
    # 关联模型展示
    inlines = [
        Goods_skuAdminInLine,
    ]


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    pass


# 关联活动专区商品
class Activity_areaAdminInline(admin.TabularInline):
    model = Activity_goods
    extra = 5
    fields = [ 'goods_sku']


# 首页专区活动
@admin.register(Activity_area)
class Activity_areaAdmin(admin.ModelAdmin):
    inlines = [
        Activity_areaAdminInline,
    ]


# 首页活动
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
