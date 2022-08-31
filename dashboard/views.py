from distutils.command.upload import upload
from email.mime import image
from multiprocessing import context
from os import stat
from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from Users.models import User 
import datetime
from .models import Order, Product 
from .forms import ProfileUpdateForm , UserUpdateForm , ProductUpdateForm 
from Shopfizz.models import OrderDetail , OrderItem, Status
# Create your views here.



@login_required(login_url='dashboard/login')
def dashboard(request):
    if request.user.is_seller==True:
        items=Product.objects.filter(seller=request.user.seller_profile)
        allorders=[]
        orders=OrderItem.objects.all()
        for my_orders in orders:
            if my_orders.seller==request.user.seller_profile :
                allorders.append(my_orders)
        length=len(items)
        context={
        'length':length,
        'items':items,
        'allorders':allorders
    }
        return render (request , 'dashboard/home.html' , context)
    else:
        return render (request , 'dashboard/login.html')


#User authentication
def loginUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username , password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None and user.is_seller==True:
            login(request , user)
            return render(request , 'dashboard/home.html')
        else:
            return redirect('dashboard-login')
    return render(request , 'dashboard/login.html')

def logoutUser(request):
        logout(request)
        return redirect('dashboard-login')


#Registeration

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        user=User.objects.create(username=username , password=password1 ,  first_name=first_name , last_name=last_name , email=email , is_seller=True)
        user.set_password(password1)
        user.save()
        return redirect('dashboard-login')
    return render(request , 'dashboard/register.html' , )

@login_required(login_url='dashboard/login')
def product(request):
    if request.method=='POST' and request.FILES['image']:
        image=request.FILES['image']
        name=request.POST.get('name')
        category=request.POST.get('category')
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        prod=Product(name=name , category=category , quantity=int(quantity) , price=price , desc=desc ,image=image, seller=request.user.seller_profile)

        prod.save()
 
    items=Product.objects.filter(seller=request.user.seller_profile)
    length=len(items)
    context={
        'items':items,
        'range':range(1 , length),
        'length':length,
    }
    return render(request , 'dashboard/product.html' , context)


@login_required(login_url='dashboard/login')
def product_delete(request , id):
    req_item=Product.objects.get(id=id)
    if request.method=='POST':
        req_item.delete()
        return redirect('dashboard-product')
    return render(request , 'dashboard/product_delete.html')


@login_required(login_url='dashboard/login')
def product_update(request , id):
    req_item=Product.objects.get(id=id)
    if request.method=='POST':
        form=ProductUpdateForm(request.POST ,request.FILES , instance=req_item )
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('dashboard-product')
        else:
            print('invalid')
    else:
        form=ProductUpdateForm(instance=req_item)
    context={
        'form':form
    }    
    return render(request , 'dashboard/product_update.html' , context)
    
@login_required(login_url='dashboard/login')
def order(request):
    allorders=[]
    items=OrderItem.objects.all()
    for my_orders in items:
        if my_orders.seller==request.user.seller_profile and my_orders.order.paid_status=='Paid':
            order_detail=my_orders.order

            customer_name=order_detail.customer_name
            date=order_detail.date
            shipping_date=date + datetime.timedelta(days=3)
            product=my_orders.product_id
            quantity=my_orders.quantity
            product_id=my_orders.product_id
            status=my_orders.status
            allorders.append({'customer_name':customer_name , 'product': product , 'quantity':quantity , 'product_id':product_id ,'status':status , 'deadline':shipping_date})

        else:
            continue
    length=len(allorders)
    context={
        'allorders':allorders,
        'length':length
    }
    return render(request , 'dashboard/order.html' , context)

@login_required(login_url='dashboard/login')
def order_detail(request , id):
    products=OrderItem.objects.filter(product_id=id)
    for prod in products:
        order_detail=prod.order
        prod_id=id
        order_id=order_detail.order_id 
        customer_name=order_detail.customer_name
        net_amount=prod.price
        address=order_detail.Address
        state=order_detail.state
        city=order_detail.city
        zip=order_detail.zip 
        date=order_detail.date 
        status=prod.status
        context={'order_id': order_id ,'product_id':prod_id ,'customer_name':customer_name , 'address':address , 'state':state , 'city':city ,'zip': zip , 'net_amount':net_amount , 'date': date , 'status':status
    }
    print(context)
    return render(request , 'dashboard/order_display.html' , context)


@login_required(login_url='dashboard/login')
def profile(request):
    return render(request , 'dashboard/profile.html')

    
@login_required(login_url='dashboard/login')
def profile_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST ,request.FILES, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST ,request.FILES, instance=request.user.seller_profile)
        if user_form.is_valid:
            user_form.save()
        if profile_form.is_valid:
            profile_form.save()
            return redirect('dashboard-profile')
  
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.seller_profile )

    context={
            'user_form':user_form,
            'profile_form':profile_form
        }
    return render(request , 'dashboard/profile_update.html' , context)