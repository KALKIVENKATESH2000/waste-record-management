from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def warpper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        elif request.user.is_authenticated == None:
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    
    return warpper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def warpper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not to view this page')
        return warpper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
    
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return # <- return response here (possibly a redirect to login page?)
    return wrapper_function