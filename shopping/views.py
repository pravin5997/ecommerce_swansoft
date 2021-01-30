from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Product, Categorys, User_cart, UserCartItem, Address, OrderItem, Order, Profile
from django.views.generic.list import ListView, View
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as authorize
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView
from .forms import ProfileForm
from django.urls import reverse
from django.core.mail import send_mail

    

class ProfileView(CreateView):
    model = Profile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('home')


class ProfileUpdateView(UpdateView): 

    model = Profile 
    form_class = ProfileForm
    success_url = "/"
    
    def get_queryset(self):
        id = self.kwargs['pk']
        
        return Profile.objects.filter(pk = id)


class Login(View):
   
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, self.template_name)

    def post(self, request):
        uname = request.POST["username"]
        upass = request.POST['password']
        user = authenticate(username = uname, password = upass)
        if user is None:
            messages.info(request, "Username or Password in not correct")
            return redirect('/login/')
        else:
            authorize(request,user)
            return redirect('/')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/login/")



class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['product'] = Product.objects.all()
        return context

    def post(self,request): 
        quantity = request.POST.get("qty")
        product_id = request.POST.get("product")
       
        prod = Product.objects.get(id=product_id)
       
       
        sub_total = round(int(prod.price) * int(quantity), 4)
        
        cart_obj = User_cart.objects.filter(user=request.user)
        cart = []
        if cart_obj:
            cart= User_cart.objects.get(user=request.user)
        else:
            cart =User_cart.objects.create(user = request.user)
            cart.save()
        cart_prod = UserCartItem.objects.filter(product=prod)
        if cart_prod:
            for cart_prods in cart_prod:
                cart_prods.quantity += int(quantity)
                sub_total = round(int(prod.price) * int(cart_prods.quantity), 4)
                cart_prods.sub_total = sub_total
                cart_prods.save()
        else:
            UserCartItem.objects.create(user_cart = cart, product = prod, quantity = quantity, price_per_unit= prod.price, sub_total=sub_total)
        cart_total = 0
        cart_item_obj = UserCartItem.objects.filter(user_cart=cart)
        if cart_item_obj:
            for i in cart_item_obj:
                cart_total += i.sub_total
            cart.total = cart_total
            cart.save()
        
        return render(request, "home.html", {"product": Product.objects.all()})


class Product_list(ListView):
    def get(self, request, name):
        
        categ = Categorys.objects.get(name=name)
       
        pro = categ.product_category.all()
        
        return render(request, "category.html", {"brand": name, "product": pro})

    def post(self, request, name):
        categ = Categorys.objects.get(name=name)
        pro = categ.product_category.all()
        quantity = request.POST.get("qty")
        product_id = request.POST.get("product")
        prod = Product.objects.get(id=product_id)
        sub_total = round(int(prod.price) * int(quantity), 4)
        
        cart_obj = User_cart.objects.filter(user=request.user)
        cart = []
        if cart_obj:
            cart= User_cart.objects.get(user=request.user)
        else:
            cart =User_cart.objects.create(user = request.user)
            cart.save()
        cart_prod = UserCartItem.objects.filter(product=prod)
        if cart_prod:
            for cart_prods in cart_prod:
                cart_prods.quantity += int(quantity)
                sub_total = round(int(prod.price) * int(cart_prods.quantity), 4)
                cart_prods.sub_total = sub_total
                cart_prods.save()
        else:
            UserCartItem.objects.create(user_cart = cart, product = prod, quantity = quantity, price_per_unit= prod.price, sub_total=sub_total)
        cart_total = 0
        cart_item_obj = UserCartItem.objects.filter(user_cart=cart)
        if cart_item_obj:
            for i in cart_item_obj:
                cart_total += i.sub_total
            cart.total = cart_total
            cart.save()
        
        return render(request, "category.html", {"brand": name, "product": pro})
        
        
class Product_details(View):
    def get(self, request, id):
        
        prod = Product.objects.get(id=id)
        
        return render(request, "product_details.html", {"product": prod})

    def post(self,request, id): 
        quantity = request.POST.get("qty")
        prod = Product.objects.get(id=id)
        sub_total = round(int(prod.price) * int(quantity), 4)
    
        cart_obj = User_cart.objects.filter(user=request.user)
        cart = []
        cart_total = None
        if cart_obj:
            cart= User_cart.objects.get(user=request.user)
        else:
            cart =User_cart.objects.create(user = request.user)
            cart.save()
        cart_prod = UserCartItem.objects.filter(product=prod)
       
        if cart_prod:
            for cart_prods in cart_prod:
                cart_prods.quantity += int(quantity)
                sub_total = round(int(prod.price) * int(cart_prods.quantity), 4)
                cart_prods.sub_total = sub_total
                cart_prods.save()
        else:
            UserCartItem.objects.create(user_cart = cart, product = prod, quantity = quantity, price_per_unit= prod.price, sub_total=sub_total)
        
        cart_total = 0
        cart_item_obj = UserCartItem.objects.filter(user_cart=cart)
        if cart_item_obj:
            for i in cart_item_obj:
                cart_total += i.sub_total
            cart.total = cart_total
            cart.save()
        
        return render(request, "product_details.html", {"product": prod})

        

class CartView(ListView):
    def get(self, request):
        cart_total = 0
        
        if request.user.is_authenticated:
            cart_user = User_cart.objects.get(user=request.user)
            cart_item = cart_user.cart_item.all()

            pro_id = request.GET.get('product_id')
            pro_qty = request.GET.get('product_qty')
            if pro_id and pro_qty:
                cart_items_total= 0
                cart_edit = UserCartItem.objects.get(id=pro_id)
                cart_edit.quantity = pro_qty
                cart_edit.sub_total = round(int(cart_edit.product.price) * int(pro_qty), 4)
                cart_edit.save()

                for item in cart_item:
                    cart_items_total += item.sub_total
                    cart_user.total = cart_items_total
                    cart_user.save()
                return JsonResponse(data={"cart_sub_total":cart_edit.sub_total,"cart_id":cart_edit.id, "carts_total":cart_user.total}, status=200)
            return render(request, "cart.html", {"cart_item": cart_item, "cart_total":cart_user.total})
        else:
            return redirect('/login/')
            

    
class ShippingAddress(View):
    def get(self, request):
        cart = User_cart.objects.get(user=request.user)
        cart_prod = cart.cart_item.all()
        
        return render(request, "shipping_address.html", {"cart_total":cart.total, "cart_prod":cart_prod})

    def post(self, request):
        cart = User_cart.objects.get(user=request.user)
        cart_prod = cart.cart_item.all()
        cart_product = list(cart.cart_item.all().values_list("product_id", flat=True))
        prod_list = Product.objects.filter(id__in=cart_product)
        address_line1 = request.POST.get("add1")
        address_line2 = request.POST.get("add2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        zip_code = request.POST.get("zip")

        current_address = Address.objects.create(user=request.user, line1=address_line1, line2=address_line2, city=city, state=state, country=country, zip_code=zip_code)
        user_ord = Order.objects.create(user=request.user, shipping_address=current_address, total=cart.total)
        for cart_prod_ord in prod_list:
            user_ord_item = OrderItem(order=user_ord, product=cart_prod_ord)
            user_ord_item.save()
        
        user_this_order = OrderItem.objects.filter(order = user_ord)
        cart_prod.delete()
        
        send_mail("Your order completed",
            'your order id is '+str(user_ord.id),
            "admin123@gmail.com",
            ['dabhi123@gmail.com'],
            fail_silently= False
            )
        print("sdfsdfdsf",cart.total)
        return render(request, "conform_order.html", {"cart_total":cart.total, "user_ord":user_ord, "current_address":current_address, "cart_prod":cart_prod, 'user_this_order':user_this_order })