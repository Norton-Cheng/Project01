# 编写限制器函数
# 限制器本质就是一个判断函数
# 参数是函数
from django.shortcuts import redirect
def login(func):
    def login_func(request,*args):
        if 'sid' in request.session:
            return func(request,*args)
        else:
            response= redirect('/dailyfresh/login/')
            # request.get_full_path() 获取请求的路径
            response.set_cookie('url',request.get_full_path())
            return response
    return  login_func