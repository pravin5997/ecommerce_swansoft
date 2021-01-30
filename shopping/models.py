from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="user_profile", on_delete = models.CASCADE)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    mobile = models.CharField(max_length=15)
    profile = models.ImageField(blank=True, upload_to='profile/', null=True)
    alternate_mobil_number = models.CharField(max_length=15)

    def __str__(self):
        return (self.first_name)

    

class Categorys(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=55)
    category = models.ForeignKey(Categorys, related_name="product_category", on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, upload_to='product/', null=True)
    status = models.BooleanField(default=True)
   
    
    def __str__(self):
        return self.name


class User_cart(models.Model):
    user = models.ForeignKey(User, related_name="cart", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class UserCartItem(models.Model):
    user_cart = models.ForeignKey(User_cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_cart_item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}"

class Order(models.Model):
    user = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey('Address', related_name='order_shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "{}".format(self.user.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return "{}".format(self.order.id)


class Address(models.Model):
    user = models.ForeignKey(User, related_name="adress", on_delete=models.CASCADE)
    line1 = models.CharField(max_length=50, default="")
    line2 = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    country = models.CharField(max_length=25)
    zip_code = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.line1, self.city)

   