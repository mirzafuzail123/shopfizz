from django.contrib import admin
from.models import Customer_Profile, OrderDetail ,OrderItem
# Register your models here.


class OrderItemTabularInLine(admin.TabularInline):
    model=OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTabularInLine]
    list_display=['customer_name' , 'order_id' , 'paid_status' ]
    list_filter=('paid_status',)


admin.site.register(Customer_Profile)
admin.site.register(OrderDetail , OrderAdmin )
admin.site.register(OrderItem )