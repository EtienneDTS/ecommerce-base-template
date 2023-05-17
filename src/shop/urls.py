from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import home_view, product_detail, add_to_cart, cart, remove_from_cart, update_selected_status, remove_from_cart_dropdown, add_review, get_product_variant_url, update_variant_detail, get_cart_data
from Ecommerce import settings


app_name = "shop"

urlpatterns = [
    path("shop/<str:category>/", home_view, name="home_shop"),
    path("shop/<str:slug>/<str:variant_slug>/<str:product_id>/<str:variant_id>/", product_detail, name="product_detail"),
    path("shop/update/url/<str:product_id>/", get_product_variant_url, name="get_product_variant_url"),
    path("shop/update/<str:product_id>/", update_variant_detail, name="update_variant_detail"),
    path("add-to-cart/<str:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("remove/<str:product_id>/<str:variant_id>/", remove_from_cart, name="remove_from_cart"),
    path("remove_dropdown/<int:cart_product_id>/", remove_from_cart_dropdown, name="remove_from_cart"),
    path("update_selected_status/", update_selected_status, name="update_selected_status"),
    path("add_review-<str:slug>/", add_review, name="add_review"),
    path("shop/get_cart_data", get_cart_data, name="get_cart_data"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

