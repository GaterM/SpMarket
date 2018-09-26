from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel

is_on_sale_choices = (
    (0, "下架"),
    (1, "上架"),
)

# 商品分类
class Goods_category(BaseModel):
    cate_name = models.CharField(max_length=50, verbose_name='分类名')
    cate_synopsis = models.CharField(max_length=100, verbose_name='分类简介', null=True, blank=True)

    class Meta:
        db_table = 'Goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cate_name


# 商品sku表
class Goods_sku(BaseModel):
    goods_name = models.CharField(max_length=50, verbose_name='商品名称')
    synopsis = models.CharField(max_length=100, verbose_name='简介', null=True, blank=True)
    goods_price = models.DecimalField(decimal_places=2, verbose_name='商品价格', max_digits=9)
    unit = models.ForeignKey(to='Goods_unit', verbose_name='商品单位')
    Stock = models.IntegerField(verbose_name='库存', default=0)
    sales_volume = models.IntegerField(verbose_name='销量', default=0)
    LOGO = models.ImageField(verbose_name='logo图片', upload_to='goods/%Y%m/%d')
    grounding = models.BooleanField(verbose_name='是否上架',choices=is_on_sale_choices,default=0)
    goods_cate = models.ForeignKey(to='Goods_category', verbose_name='商品分类')
    goods_spu = models.ForeignKey(to='Goods_spu', verbose_name='商品spu')

    class Meta:
        db_table = 'Goods_sku'
        verbose_name = '商品sku'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name


# 商品spu表
class Goods_spu(models.Model):
    spu_name = models.CharField(max_length=20, verbose_name='商品spu名称')
    # detail = models.TextField(verbose_name='商品详情')
    detail = RichTextUploadingField(verbose_name='商品详情')

    class Meta:
        db_table = 'Goods_spu'
        verbose_name = '商品spu'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.spu_name


# 单位表
class Goods_unit(BaseModel):
    unit_name = models.CharField(max_length=10, verbose_name='单位名')

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "商品单位"
        verbose_name_plural = verbose_name


# 商品相册
class Goods_album(BaseModel):
    image_addr = models.ImageField(verbose_name='图片地址',upload_to='goods/%Y%m/%d')
    goods_sku = models.ForeignKey(to='Goods_sku', verbose_name='商品id')

    class Meta:
        db_table = 'Goods_album'
        verbose_name = '商品相册'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '商品：%s的相册' % self.goods_sku.goods_name


# 首页轮播商品
class Broadcast(BaseModel):
    name = models.CharField(max_length=50, verbose_name='名称')
    good_sku = models.ForeignKey(to='Goods_sku', verbose_name='商品sku_id')
    image = models.ImageField(verbose_name='轮播图', upload_to='broadcast/%Y%m/%d')
    order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'Broadcast'
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页活动表
class Activity(models.Model):
    name = models.CharField(max_length=150, verbose_name='活动名称')
    image = models.ImageField(verbose_name='活动图片', upload_to='activity/%Y%m/%d')
    url = models.CharField(max_length=200, verbose_name='地址')

    class Meta:
        db_table = 'Activity'
        verbose_name = '首页活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页活动专区
class Activity_area(BaseModel):
    name = models.CharField(max_length=50, verbose_name='专区名称')
    describ = models.TextField(verbose_name='描述', null=True, blank=True)
    order = models.IntegerField(verbose_name='排序', default=0)
    is_on_sale = models.BooleanField(verbose_name='是否上架', choices=is_on_sale_choices, default=0)

    class Meta:
        db_table = 'Activity_area'
        verbose_name = '首页活动专区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页专区活动商品
class Activity_goods(BaseModel):
    area = models.ForeignKey(to='Activity_area', verbose_name='专区id')
    goods_sku = models.ForeignKey(to='Goods_sku',verbose_name='专区商品sku_id')

    class Meta:
        db_table = 'Activity_goods'
        verbose_name = '首页活动商品'
        verbose_name_plural = verbose_name