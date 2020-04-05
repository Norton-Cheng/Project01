from django.db import models
from df_goods.models import Goodsinfo
from df_user.models import Userinfo

# Create your models here.
class Cartinfo(models.Model):
    # 用户id
    user=models.ForeignKey('df_user.Userinfo',on_delete=models.CASCADE)
    # 商品id  model属性就是商品，外观联会自动转换成goods
    goods=models.ForeignKey('df_goods.Goodsinfo',on_delete=models.CASCADE)
    # 商品数量
    count = models.IntegerField()
    # 是否删除
    isDelete=models.BooleanField(default=False)
    class Meta:
        db_table='cartinfo'