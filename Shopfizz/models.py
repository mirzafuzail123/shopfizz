from datetime import datetime
from django.db import models
from Users.models import User
from dashboard.models import Product , Seller_Profile
# Create your models here.



class Customer_Profile(models.Model):
    customer=models.OneToOneField(User , on_delete=models.CASCADE ,  null=True )
    phone=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    Address=models.CharField(max_length=200 , null=True)
    
    def __str__(self) :
        return f'{self.customer.username} - Profile'

p_status=(
     ('Not Paid' , 'Not Paid'),
    ('Paid' , 'Paid'),
)
Status=(
    ('Order Confirmed' , 'Order Confirmed'),
    ('Picked by courier' , 'Picked by courier'),
    ('Ready to pickup', 'Ready to pickup'),
)
class OrderDetail(models.Model):
    order_id=models.AutoField(primary_key=True)
    customer_name=models.ForeignKey(User, models.CASCADE)
    phone=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    Address=models.CharField(max_length=200 , null=True)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zip=models.IntegerField ()
    total=models.FloatField()
    date=models.DateField(default=datetime.now)
    status=models.CharField(choices=Status , max_length=50 , null=True)
    paid_status=models.CharField(choices=p_status, max_length=50,  default='Not paid')

    def __str__(self) :
        return f'{self.order_id}'

Status=(
    ('Pending' , 'Pending'),
    ('Shipped' , 'Shipped'),
    ('Deliverd' , 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class OrderItem(models.Model):
    order=models.ForeignKey( OrderDetail, on_delete=models.CASCADE )
    product_id=models.ForeignKey(Product , on_delete=models.CASCADE ,   null=True)
    product=models.CharField(max_length=200)
    quantity=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    seller= models.ForeignKey(Seller_Profile , on_delete=models.CASCADE , null=True)
    status=models.CharField(choices=Status , max_length=50 , default='Pending')
    def __str__(self) :
        return f'{self.product_id}'