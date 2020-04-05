from django.conf.urls import url
from df_user.views import *

urlpatterns=[
    url(r'^login/$',login,name='login'),
    url(r'^register/$',register,name='register'),
    url(r'^register_handle/$',register_handle,name='rhandle'),
    url(r'^login_handle/$',login_handle,name='lhandle'),
    url(r'^info/$',info,name='info'),
    url(r'^order/$',order,name='order'),
    url(r'^site/$',site,name='site'),
    url(r'^logout/$',logout,name='logout'),
]