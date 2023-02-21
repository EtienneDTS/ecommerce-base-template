from django.contrib import admin
from django.urls import path, include

from .views import home_view

app_name = "shop"

urlpatterns = [
    path("home/", home_view, name="home")
    
]

