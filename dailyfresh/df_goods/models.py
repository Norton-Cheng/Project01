from django.db import models
from tinymce.models import HTMLField

# Create your models here.

# 商品分类模型：介绍有哪些种类商品
class Typeinfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    class Meta:
        db_table:'typeinfo'

# 商品类
class Goodsinfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gprice=models.DecimalField(max_digits=7,decimal_places=2)
    gpicture=models.CharField(max_length=20)
    gintro=models.CharField(max_length=200)
    gunit=models.CharField(max_length=20,default="500g")
    gclick=models.IntegerField()
    gkucun=models.IntegerField(default=0)

    # HTMLField:超文本类型（视频、图片、音乐、文字...）
    gcontent=HTMLField()

    # 多表关联
    gtype=models.ForeignKey('Typeinfo',on_delete=models.CASCADE)
    class Meta:
        db_table='goodsinfo'

