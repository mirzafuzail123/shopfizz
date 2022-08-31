from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from Shopfizz import views
from shoping_cart import views as c_views
from dashboard import views as d_views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('' , views.index , name='home'),
    path('register' , views.register , name='shopfizz-register'),
    path('login' , views.loginUser , name='shopfizz-login'),
    path('logout' , views.logoutUser , name='shopfizz-logout'),
    path('tracker' , views.tracker , name='shopfizz-tracker'),
    path('search' , views.search , name='shopfizz-search'),



    path('product_display/<int:id>' , views.product_display , name='shopfizz-product_display'),
    path('product_display/dashboard' , d_views.dashboard , name='product_display-home'),
    path('product_display/register' , views.register , name='shopfizz-register-product_display'),
    path('product_display/login' , views.loginUser , name='shopfizz-login-product_display'),
    path('product_display/logout' , views.logoutUser , name='shopfizz-logout-product_display'),
    path('/product_display/cart/add/<int:id>/ ', c_views.cart_add, name='product_display_cart_add'),



]

