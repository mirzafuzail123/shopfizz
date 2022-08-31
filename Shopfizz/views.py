from math import ceil
from multiprocessing import context
from nis import cat
from pickletools import read_uint1
from unicodedata import category
from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from Shopfizz.forms import CreateUser
from django.contrib.auth import authenticate, login , logout
from Shopfizz.models import OrderDetail, OrderItem
from dashboard.models import Product
import datetime

# Create your views here.

def index(request):
   

    allprod=[]
    categories=Product.objects.values('category')
    cat_set=set()
    for category in categories:
        cat_set.add(category['category'])
    for cat in cat_set:
        prod=Product.objects.filter(category=cat)
        length=len(prod)
        no_slides=length//4 + ceil(length/4 - length//4)
        allprod.append([prod , range(1 , no_slides , no_slides)])
    context={
        'allprod':allprod
    }   
    return render(request , 'shopfizz/index.html' , context)



def loginUser(request):
    if request.method=='POST':
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            raise ValueError ('Please enter correct credentials')
    return render(request , 'shopfizz/login.html')

def logoutUser(request):
    logout(request)
    return redirect ('home')



def register(request):
    if request.method=='POST':
        form=CreateUser(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=CreateUser()
    context={
        'form':form
    }
    return render(request , 'shopfizz/register.html', context)

def product_display(request , id):
    product=Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request , 'shopfizz/product_display.html' , context)

def tracker(request):
    items=[]
    customer=request.user
    orders=OrderDetail.objects.filter(customer_name=customer)
    for order in orders:
        prod=OrderItem.objects.filter(order=order)
        date=order.date
        shipping_date=date + datetime.timedelta(days=7)
        items.append([prod , shipping_date])
       
    #print(detail)
    context={
        'items':items,
    }
    print(context)
    return render(request , 'shopfizz/tracker.html' , context)


def search(request):
    query=request.GET.get('query')
    product=Product.objects.filter(name__icontains=query)
    length=len(product)
    context={
        'searchedproduct':product,
        'length':length
    }
    return render(request , 'shopfizz/search.html' ,context)


