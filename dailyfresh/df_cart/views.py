from django.shortcuts import render,redirect
from df_user import user_yanzheng
from df_cart.models import Cartinfo
from django.http import JsonResponse

# Create your views here.
# 购物车
@user_yanzheng.login
def cart(request):
    # 根据用户id,获取购物车信息
    carts=Cartinfo.objects.filter(user_id=request.session.get('sid'))
    context={
        'carts':carts,
    }
    return render(request, 'df_cart/cart.html',context)

# 加入购物车
@user_yanzheng.login
def addCart(request,gid,count):
    # 将加入购物车商品信息写入数据表
    uid=request.session.get('sid')
    carts=Cartinfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)!=0:
        # 有购物车
        cart=carts[0]
        cart.count += int(count)
    else:
        cart=Cartinfo()
        cart.user_id=int(uid)
        cart.goods_id=int(gid)
        cart.count=int(count)
    cart.save()
    # 判断-如果ajax请求，添加动画
    if request.is_ajax():
        # 请求函数：必须返回响应对象，可以返回JsonResponse(数据),将数据写入浏览器里面，但是不做相关跳转
        # 获取数量，放入json里面，通过ajax调用时，显示数量
        ccount=Cartinfo.objects.filter(user_id=uid).count()
        from django.http import JsonResponse
        return JsonResponse({'ccount':ccount})


    # 否则，重定向到cart页面
    return redirect('/dailyfresh/cart/')

# 编辑购物车
@user_yanzheng.login
def edit(request,cid,newcount):
    try:
        cart=Cartinfo.objects.get(id=int(cid))
        cart.count=newcount
        cart.save()
        data={'ok':0}
    except:
        data = {'ok': int(newcount)}
    return JsonResponse(data)

# 删除
def delete_cart(request,cid):
    try:
        Cartinfo.objects.get(pk=int(cid)).delete()
        data={'ok':1}
    except Exception as res:
        data = {'ok': 0}
    return JsonResponse(data)










