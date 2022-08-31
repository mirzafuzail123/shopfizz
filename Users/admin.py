from django.contrib import admin
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model=User
    add_form=CustomUserCreationForm
    list_display=('username' , 'email' , 'is_seller' , 'is_staff')
    list_filter=('is_seller' , 'is_staff')
    fieldsets = (
        *UserAdmin.fieldsets,
        ('User Role',
         {'fields': 
            (
                'is_customer', 
                'is_seller'
            )}
        ),

    )
  
    print(len(fieldsets[4]))
# Register your models here.
admin.site.register(User , CustomUserAdmin)
