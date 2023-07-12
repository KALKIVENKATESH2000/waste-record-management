
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import UserForm
from django.contrib.admin.views.decorators import staff_member_required
from master.decorator import unauthenticated_user, admin_only, allowed_users

@unauthenticated_user
def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        

    context = {'form':form}
    return render(request, 'register_page.html', context)
@unauthenticated_user 
def loginPage(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password, is_active=True)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login_page.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')