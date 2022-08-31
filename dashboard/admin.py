from django.contrib import admin
from dashboard.models import Product , Order , Seller_Profile

admin.site.site_header='Shopfizz'

class ProductAdmin(admin.ModelAdmin):
    list_display=('name' , 'quantity' , 'category' , 'seller')
    list_filter=('category', 'seller')

# Register your models here.
admin.site.register(Product , ProductAdmin)
admin.site.register(Order)
admin.site.register(Seller_Profile)