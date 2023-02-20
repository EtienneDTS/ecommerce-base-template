from django.contrib import admin
from shop.models import Product
from accounts.models import CustomUser

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "image",
    )
    
    list_editable = (
        "price",
    )
    
    list_display_links = ("name",)
    
    field_labels = {
        'name': 'Nom',
        'description': 'Description',
        'price': 'Prix',
        'image': 'Image'
    }

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass
