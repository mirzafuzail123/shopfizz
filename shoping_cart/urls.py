from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from shoping_cart import views
urlpatterns = [
    path('' , views.cart_detail , name='cart-detail'),
    path('/add/<int:id>/', views.cart_add, name='cart_add'),
    path('/buy/<int:id>/', views.buy_now, name='buy_now'),

    path('/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('/cart_clear/', views.cart_clear, name='cart_clear'),
    path('/checkout/', views.checkout, name='cart_checkout'),

    path('/paymentsuccess' , views.PaymentSuccess , name='cart-payment-success'),
    path('/paymentcancel' , views.PaymentCancel , name='cart-payment-cancel'),
    path('/webhooks/stripe' , views.my_webhook_view , name='cart-webhook'),


]