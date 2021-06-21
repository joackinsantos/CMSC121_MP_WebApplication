from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 

from . forms import CreateUserForm

# Create your views here.

def home(request):
    return render(request, "planter/home.html")

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request, 'planter/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'planter/login.html', context)
