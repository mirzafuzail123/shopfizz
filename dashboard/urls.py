from re import template
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path , include
from dashboard import views

urlpatterns = [
    path('' , views.dashboard , name='dashboard'),
    path('/register' , views.register , name='dashboard-register'),
    path('/login' , views.loginUser , name='dashboard-login'),
    path('/logout' , views.logoutUser , name='dashboard-logout'),
    path('/register' , views.register , name='dashboard-register'),
    path('/product' , views.product , name='dashboard-product'),
    path('/product/delete/<int:id>' , views.product_delete , name='dashboard-product_delete'),
    path('/product/update/<int:id>' , views.product_update , name='dashboard-product_update'),

    path('/order' , views.order , name='dashboard-order'),
    path('/order/order_display/<int:id>' , views.order_detail , name='dashboard-order_display'),

    path('/profile' , views.profile , name='dashboard-profile'),
    path('/profile_update' , views.profile_update , name='dashboard-profile_update')





]