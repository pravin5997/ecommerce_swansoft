from django.contrib import admin
from .models import Categorys, Product, Profile,User_cart,UserCartItem, OrderItem, Address, Order

# Register your models here.

admin.site.register(Categorys)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(User_cart)
admin.site.register(UserCartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)