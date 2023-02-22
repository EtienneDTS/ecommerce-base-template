from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import home_view
from Ecommerce import settings


app_name = "shop"

urlpatterns = [
    path("shop/", home_view, name="home_shop")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

