from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/planter/images/icons/favicon.ico')),
    path('shop/', views.shop, name="shop"),
    path('account/', views.account, name="account")
]