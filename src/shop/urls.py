from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import home_view, product_detail, add_to_cart, cart, remove_from_cart, update_selected_status, add_review
from Ecommerce import settings


app_name = "shop"

urlpatterns = [
    path("shop/", home_view, name="home_shop"),
    path("shop/<str:slug>/", product_detail, name="product_detail"),
    path("add-to-cart-<str:slug>", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("remove-<str:slug>/", remove_from_cart, name="remove_from_cart"),
    path("update_selected_status/", update_selected_status, name="update_selected_status"),
    path("add_review-<str:slug>/", add_review, name="add_review"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

