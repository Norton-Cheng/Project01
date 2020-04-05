from django.conf.urls import url
from df_goods.views import *
urlpatterns=[
    url(r'^index/$',index,name='index'),
    url(r'^list(\d+)_(\d+)_(\d+)/$',list,name='list'),
    url(r'^detail/$',detail,name='detail'),
]