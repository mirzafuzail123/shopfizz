from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from Users.models import User
#Registration form:
class CreateUser(UserCreationForm):
    email=forms.EmailField()
    
    class Meta:
        model=User
        fields=['username' , 'email' , 'password1' , 'password2' ]