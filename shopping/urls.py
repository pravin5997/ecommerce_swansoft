from django.urls import path
from .views import Home, Product_list, Product_details, CartView, Login, ShippingAddress, Logout, ProfileView, ProfileUpdateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
  
    path("", Home.as_view(), name="home"),
    path("product/<str:name>/", Product_list.as_view(), name="product_list"),
    path("product_details/<int:id>/", Product_details.as_view(), name="product_details"),
    path("cart_list/", CartView.as_view(), name="cart"),
    path("login/", Login.as_view(), name="login"),
    path("shipping/", ShippingAddress.as_view(), name="shipping"),
    path("logout/", Logout.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="create_profile"),
    path("profile/<int:pk>/", ProfileUpdateView.as_view(), name = "update_profile"),
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)