from django.shortcuts import render
from df_goods.models import *
from django.core.paginator import *
from df_cart.models import Cartinfo
# Create your views here.

# 首页
def index(request):
    # 提取每一种类型最新、点击量最高的4个商品
    all_types = Typeinfo.objects.all()
    # 最新：新鲜水果
    newfruits=all_types[0].goodsinfo_set.order_by("-id")[0:4]
    # 人气最高：新鲜水果
    hotfruits=all_types[0].goodsinfo_set.order_by("-gclick")[0:4]
    context={
        'title':'商品首页',
        'newfruits':newfruits,
        'hotfruits':hotfruits,
        'carts_count':Cartinfo.objects.filter(user_id=request.session.get('sid')).count()
    }
    return render(request, 'df_goods/index.html',context)

# 列表
def list(request,tid,sort,index):
    # 根据类型获取2个新品
    goodstype=Typeinfo.objects.get(id=int(tid))
    new_goods=goodstype.goodsinfo_set.order_by('-id')[:2]
    # 根据类型获取所有商品
    # 默认
    if sort=='1':
        all_goods=goodstype.goodsinfo_set.order_by('id')
    # 人气
    elif sort=='2':
        all_goods = goodstype.goodsinfo_set.order_by('gprice')
    # 价格
    else:
        all_goods = goodstype.goodsinfo_set.order_by('-gclick')
    # 创建分页对象
    pn=Paginator(all_goods,4)
    # 创建页面对象
    page_goods=pn.page(index)
    context = {
        'title': '商品列表',
        'new_goods': new_goods,
        'all_goods': all_goods,
        'goodstype': goodstype,
        'sort':sort,
        'page_goods':page_goods,
        'pn':pn,
    }
    return render(request, 'df_goods/list.html',context)

# 详情
def detail(request):
    goods_id=request.GET.get('id')
    # 获取商品
    goods=Goodsinfo.objects.get(id=int(goods_id))
    goods.gclick += 1
    goods.save()
    # 根据商品获取类型
    goods_type = Typeinfo.objects.get(id=goods.gtype_id)
    # 新品
    new_goods = goods_type.goodsinfo_set.order_by('-id')[:2]
    context = {
        'title': '商品详情',
        'goods': goods,
        'goods_type': goods_type,
        'new_goods': new_goods,
    }
    response= render(request, 'df_goods/detail.html',context)

    # 设置最近浏览的cookie
    # 将浏览器里面保存的cookie获取后转换成列表使用
    ids_str=request.COOKIES.get("ids","")
    if ids_str != '':
        ids_list= ids_str.split(',')
        # 判断是否存在，存在删除记录
        if goods_id in ids_list:
            ids_list.remove(goods_id)
        ids_list.insert(0,goods_id)
        # 判断是否长度为5
        if len(ids_list) >= 6:
            ids_list.pop()
        # 转换成功字符串
        gids=",".join(ids_list)

    else:
        gids=goods_id
    response.set_cookie('ids',gids)
    return response