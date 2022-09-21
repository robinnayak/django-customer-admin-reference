from unicodedata import name
from django.urls import path, include
from .views import AdimnUserView, CustomerUserView,LoginPage,RegisterPage,LogoutPage

urlpatterns = [
    path("", AdimnUserView, name="home"),
    
    path("customer/", CustomerUserView, name="customeruser"),
    
    path('login/',LoginPage, name="login"),
    path('logout/',LogoutPage, name="logout"),
    path('register/',RegisterPage,name="register"),
]
