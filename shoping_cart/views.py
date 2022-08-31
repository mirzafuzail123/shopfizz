from hashlib import new
from importlib.metadata import metadata
from multiprocessing import context
from unicodedata import name
from urllib import request
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from Users.models import User
from Shopfizz.models import OrderDetail , OrderItem
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from dashboard.models import Product
from dashboard.views import order, order_detail, product

# Create your views here.
@login_required(login_url="shopfizz-login")
def cart_detail(request):
    return render(request , 'cart/cart.html')


@login_required(login_url="shopfizz-login")
def cart_add(request, id):
    cart=Cart(request)
    prod=Product.objects.get(id=id)
    cart.add(product=prod)
    context={'product': prod}
    return render ( request, 'shopfizz/product_display.html' , context)


@login_required(login_url="shopfizz-login")
def buy_now(request, id):
    cart=Cart(request)
    prod=Product.objects.get(id=id)
    cart.add(product=prod)
    return redirect('cart-detail')


@login_required(login_url="shopfizz-login")
def item_clear(request, id):
    cart=Cart(request)
    prod=Product.objects.get(id=id)
    cart.remove(prod)
    return redirect('cart-detail')

@login_required(login_url="shopfizz-login")
def item_increment(request , id):
    cart=Cart(request)
    prod=Product.objects.get(id=id)
    cart.add(product=prod)
    return redirect('cart-detail')


@login_required(login_url="shopfizz-login")
def item_decrement(request , id):
    cart=Cart(request)
    prod=Product.objects.get(id=id)
    cart.decrement(product=prod)
    return redirect('cart-detail')



@login_required(login_url="shopfizz-login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart-detail")



stripe.api_key=settings.STRIPE_SECRET_KEY

@login_required(login_url="shopfizz-login")
def checkout(request):
    uid=request.session.get('_auth_user_id')
    customer=User.objects.get(id=uid)
    print(customer)
    x=request.session.get('cart')
    c_values=x.values()
    if request.method=='POST':
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address1=request.POST.get('address1')
        address2=request.POST.get('address2')
        state=request.POST.get('state')
        city=request.POST.get('city')
        zip=request.POST.get('zip')
        total=request.POST.get('total')
        order_detail=OrderDetail(customer_name=customer , phone=phone , email=email , Address=address1 + "" + address2 , state=state , city=city , zip=zip , total=total)
        order_detail.save()

        orders_list=[]
        for value in c_values:
            ordered_product= value['product_id' ]
            actual_product=Product.objects.get(id=ordered_product)
            product=value['name']
            quantity=value['quantity']
            price=value['price']
            Net_amount=quantity*int(price)
            product_id=value['product_id']
            seller=Product.objects.get(id=product_id).seller
            order_item=OrderItem( product_id=actual_product , order=order_detail , product=product ,  quantity=quantity , price=Net_amount , seller=seller)
            order_item.save()
            orders_list.append(order_item)

            #order_item.save()
        i=float(total)
        ii=int(i)
        cart = Cart(request)
        cart.clear()
        #Payment method:
        YOUR_DOMAIN='http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency':'pkr',
                        'unit_amount':ii*100 ,
                        'product_data':{
                            'name':order_detail.order_id

                        },

                    },
                    'quantity': len(orders_list),
                },
            ],
            metadata={
                'order_id':order_detail.order_id,
                'p_id_list':str(orders_list),
                    
            },
            
                
            mode='payment',
            success_url=YOUR_DOMAIN + 'cart/paymentsuccess',
            cancel_url=YOUR_DOMAIN + 'cart/paymentcancel',
        )


        return redirect(checkout_session.url, code=303)


     

    return render(request , 'cart/checkout.html' )







def PaymentSuccess(request):
    
    context={
        'payment':'success'
    }
    return render(request , 'cart/confirmation.html' , context)

def PaymentCancel(request):
    context={
        'payment':'cancel'
    }
    return render(request , 'cart/confirmation.html' , context)

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_WEBHOOK_KEY
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
# Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    order_id=session['metadata']['order_id']
    instance=OrderDetail.objects.filter(order_id=int(order_id))
    instance.update(paid_status='Paid', status='Order Confirmed')

    name=instance[0].customer_name
    details=session['customer_details']['email']

    #Inventory managemant
    order=OrderDetail.objects.get(order_id=order_id)
    items=OrderItem.objects.filter(order=order)
    print(items)
    for item in items:
        stock=item.product_id.quantity
        order_quantity=item.quantity
        new_stock=stock-order_quantity

        #updating inventory
        p_id=item.product_id.id
        print(p_id)
        prod=Product.objects.filter(id=p_id)
        print(prod)
        prod.update(quantity=new_stock)




    send_mail(
        subject='Here is your product',
        message=f'''Hey {name} ! Thanks for  purchasing..
                Your order id is {order_id} and your tracking id is {{order_id}}''',
        recipient_list=[details],
        from_email='shopfizz@gmail.com'
        
    )
  



  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(session):
  # TODO: fill me in
  print("Fulfilling order")
