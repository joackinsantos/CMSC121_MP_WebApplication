from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('update_item/', views.updateItem, name="checkout"),

    path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/planter/images/icons/favicon.ico')),
    path('shop/', views.shop, name="shop"),
    path('account/', views.account, name="account")



]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)