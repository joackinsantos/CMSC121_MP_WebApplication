from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#from django.contrib.auth.decorators import login_required

from . forms import CreateUserForm



#--HOME PAGE VIEW--
def home(request):
    return render(request, "planter/home.html")

#--REGISTER PAGE VIEW--
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Welcome to Planter, ' + user + '!')

            sendEmail(request)
            return redirect('login')

    context = {'form':form}
    return render(request, 'planter/register.html', context)


#--LOGIN PAGE VIEW--
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'planter/login.html', context)

#--LOGOUT USER--
def logoutUser(request):
    logout(request)
    return redirect('login')

#--SHOP VIEW--
def shop(request):
    return render(request, "planter/shop.html")

#--ACCOUNT VIEW--
def account(request):
    return render(request, "planter/account.html")
