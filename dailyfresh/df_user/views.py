from django.shortcuts import render,redirect
from df_user.models import Userinfo
from hashlib import sha1
from df_user import user_yanzheng

# Create your views here.
# 登录
def login(request):
    ckname=request.COOKIES.get('name','')
    context={
        'title':'登录',
        'lname':ckname,
    }
    return render(request,'df_user/login.html',context)

# 登录-处理函数
def login_handle(request):
    # 获取from表到的数据
    lname=request.POST.get('username')
    lpwd=request.POST.get('pwd')
    # 查询
    users=Userinfo.objects.filter(uname=lname)
    if len(users)==0:
        # 没有账号 -》 返回login
        context={
            'title':'登录',
            'user_error':1,
            'pass_error':0,
            'lname':lname,
            'lpwd':lpwd,
        }
        return render(request,'df_user/login.html',context)
    else:
        # 有账号 -》 密码正确重定向到home,密码错误重定向到登录页
        s1=sha1()
        s1.update(lpwd.encode('gbk'))
        jm_pwd=s1.hexdigest()
        if users[0].upwd==jm_pwd:
            from django.http import HttpResponse
            url=request.COOKIES.get('url','/dailyfresh/info/')
            response= redirect(url)
            if len(request.POST.getlist('jz'))!=0:
                response.set_cookie('name',lname)
            else:
                response.set_cookie('name','',-1)
            # 将用户的账号、id写到session里面
            request.session['sname']=lname
            request.session['sid'] = users[0].id
            return response
        else:
            context={
                'title': '登录',
                'user_error': 1,
                'pass_error': 0,
                'lname': lname,
                'lpwd': lpwd,
            }
            return render(request, 'df_user/login.html',context)

# 注册
def register(request):
    context = {
        'title': '注册'
    }
    return render(request, 'df_user/register.html',context)

# 注册-处理函数
def register_handle(request):
    # 获取form表单的数据
    rname=request.POST.get('user_name')
    rpwd=request.POST.get('pwd')
    cpwd=request.POST.get('cpwd')
    remail=request.POST.get('email')

    # 密码是否一致 -》重定向到注册页
    if rpwd!=cpwd:return ('/dailyfresh/register/')
    # 用户名是否重复 -》重定向到注册页
    if len(Userinfo.objects.filter(uname=rname)) != 0: return redirect('/dailyfresh/register/')
    # 如果没有勾选 -》 重定向到注册页
    allow=request.POST.getlist('allow')
    if len(allow)==0:return redirect('/dailyfresh/register/')
    # 密码加密
    s1=sha1()
    s1.update(rpwd.encode('gbk'))
    jm_pwd=s1.hexdigest()
    # 将数据写入数据库
    user=Userinfo()
    user.uname=rname
    user.upwd=jm_pwd
    user.uemail=remail
    user.save()
    # 重定向到登录页面
    return redirect('/dailyfresh/login/')

# info
@user_yanzheng.login
def info(request):
    # 获取到登录成功后用户的信息，传递到页面上
    sid=request.session.get('sid')
    user=Userinfo.objects.get(id=sid)
    # 获取最近浏览记录的cookie
    ids_str=request.COOKIES.get('ids','')
    # 定义空列表保存商品对象
    now_goods=[]
    if ids_str!='':
        ids_list=ids_str.split(',')
        # 根据商品id获取商品对象
        from df_goods.models import Goodsinfo
        for gid in ids_list:
            now_goods.append(Goodsinfo.objects.get(id=int(gid)))

    context={
        'user': user,
        'now_goods':now_goods,
    }
    return render(request,'df_user/user_center_info.html',context)

# order
@user_yanzheng.login
def order(request):
    return render(request,'df_user/user_center_order.html')

# site
def site(request):
    # 通过session里面的id查询到该用户
    user=Userinfo.objects.get(id=request.session.get('sid'))
    # 如果是post方式请求的
    # 提取post表单的数据
    if request.method=='POST':
        user.ureceiver=request.POST.get('sjr')
        user.uaddress=request.POST.get('address')
        user.uzipcode=request.POST.get('zipcode')
        user.uphone = request.POST.get('phone')
        user.save()
    if len(user.uphone)!=0:
        phone=user.uphone[:3]+"****"+user.uphone[-4:]
    else:
        phone=user.uphone
    context={
        'user':user,
        'phone':phone,
    }
    return render(request,'df_user/user_center_site.html',context)

# 退出
def logout(request):
    # 清空session
    request.session.flush()
    # 重定向到登录页
    return redirect('/dailyfresh/login/')



