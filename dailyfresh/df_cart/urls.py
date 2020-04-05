from django.conf.urls import url
from df_cart.views import *
urlpatterns=[
    url(r'^cart/$',cart,name='cart'),
    url(r'^addcart(\d+)_(\d+)/$',addCart,name='add'),
    url(r'^edit(\d+)_(\d+)/$',edit,name='edit'),
    url(r'^del(\d+)/$',delete_cart,name='del'),
]