from django.contrib import admin
from shop.models import Product, ProductImages, Category, CartProduct, Cart, ProductVariant, OptionName
from accounts.models import CustomUser

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "image",
    )
    
    list_editable = (
        
    )
    
    list_display_links = ("name",)
    
    field_labels = {
        'name': 'Nom',
        'description': 'Description',
        'image': 'Image'
    }

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "image",
    )
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "session_key"
    )
    
@admin.register(Category)
class CategorieAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    
@admin.register(OptionName)
class OptionNameAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        
    )
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "variant_name",
        "price"
    )