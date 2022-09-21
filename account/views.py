from django.contrib.auth.models import Group
from django.shortcuts import render,redirect
from .models import Customer
from .forms import CreateUserForm,CustomerForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

@admin_only
def AdimnUserView(request):
    customer = Customer.objects.all()
    context = {
        "customers":customer,
    }
    return render(request,'account/adminuser.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def CustomerUserView(request):
    customer = request.user.customer
    context = {
        "customer":customer
    }
    return render(request,'account/customeruser.html',context)

@unauthenticated_user
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,name = user.username,email = user.email)
            messages.success(request,'Account was created for ' + username )
            
            return redirect('login')

    context = {
        "form":form
    }
    return render(request,'account/register.html',context)

@unauthenticated_user
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("customeruser")
            # return redirect("home")
        else:
            messages.info(request, "Username or password is incorect")

    context = {
        
    }
    return render(request,'account/login.html',context)

def LogoutPage (request):
    logout(request)
    return redirect('login')