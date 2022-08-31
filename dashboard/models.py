from itertools import product
from pickle import TRUE
from django.db import models
from Users.models import User


# Create your models here.

class Seller_Profile(models.Model):
    seller=models.OneToOneField(User , on_delete=models.CASCADE ,  null=True)
    phone=models.IntegerField(null=True)
    Address=models.CharField(max_length=200 , null=True)
    image=models.ImageField(default='media/images/avatar.jpg' , upload_to='media/images/')    

    def __str__(self) :
        return f'{self.seller.username}'




Category=(
    ('Stationary', 'Stationary'),
    ('Fashion', 'Fashion'),
    ('Electronic device', 'Electronic device'),
    ('Food', 'Food'),
    ('Babies & Toys', 'Babies & Toys'),

)
class Product(models.Model):
    name=models.CharField(max_length=100, null=TRUE)
    category=models.CharField(choices=Category , max_length=80,null=TRUE )
    seller=models.ForeignKey( Seller_Profile , default=True,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField( null=TRUE)
    price=models.PositiveBigIntegerField(null=TRUE)
    desc=models.CharField(max_length=1000 , null=TRUE)
    image=models.ImageField(upload_to='media/images/')
    def __str__(self):
        return f'{self.id}'



class Order(models.Model):
    product=models.ForeignKey(Product , on_delete=models.CASCADE , null=True)
    seller=models.ForeignKey(User , models.CASCADE , null=True)
    order_quantity=models.PositiveBigIntegerField(null=True)
    date=models.DateField(auto_now=True)

    def __str__(self):
        return f' {self.product} ordered by {self.seller.username}'

