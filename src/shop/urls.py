from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import home_view, product_detail, add_to_cart, cart, remove_from_cart
from Ecommerce import settings


app_name = "shop"

urlpatterns = [
    path("shop/", home_view, name="home_shop"),
    path("shop/<str:slug>/", product_detail, name="product_detail"),
    path("add-to-cart/<str:slug>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("remove-<str:slug>/", remove_from_cart, name="remove_from_cart")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

