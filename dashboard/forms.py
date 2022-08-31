from dataclasses import fields
from unicodedata import category
from Users.models import User
from .models import Seller_Profile , Product
from django import forms

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username' , 'email' , 'first_name' , 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Seller_Profile
        fields=['Address' , 'phone' , 'image']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model= Product
        fields=['name', 'category' , 'quantity' , 'price' , 'desc','image' ]

