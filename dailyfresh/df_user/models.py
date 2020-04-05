from django.db import models

# Create your models here.
class Userinfo(models.Model):
    # 账号
    uname=models.CharField(max_length=20)
    # 密码
    upwd=models.CharField(max_length=100)
    # 邮箱
    uemail=models.CharField(max_length=50)
    # 手机号码
    uphone=models.CharField(max_length=11,default='')
    # 收件人
    ureceiver=models.CharField(max_length=20,default='')
    # 地址
    uaddress=models.CharField(max_length=100,default='')
    # 邮编
    uzipcode=models.CharField(max_length=6,default='')
    # 逻辑删除
    isDelete=models.BooleanField(default=False)
    # 元选项
    class Meta:
        db_table='userinfo'