from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "planter/home.html")

def shop(request):
    return render(request, "planter/shop.html")

def account(request):
    return render(request, "planter/account.html")
