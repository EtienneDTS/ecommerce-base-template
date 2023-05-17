from django.db import models
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Categorie"
        
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    brand = models.CharField(max_length=255, verbose_name="Marque")
    name = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.SlugField(default="", blank=True, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='shop', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.brand} - {self.name}"
    
    class Meta:
        verbose_name = "Produit"
        
    @property    
    def product_title(self):
        if self.brand:
            return f"{self.brand} - {self.name}"
        else:
            return self.name

# allow several images for one product        
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shop', blank=True, null=True)
    
    class Meta:
        verbose_name = "images de produit"
        

class OptionName(models.Model):
    name = models.CharField(max_length=50)  
    
    class Meta:
        verbose_name = "Nom de l'option de produit"   
        
    def __str__(self) -> str:
        return self.name   
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Nom du produit")
    variant_slug = models.SlugField(default="", blank=True, verbose_name="Slug de la variante")
    variant_name = models.CharField(max_length=255, verbose_name="Nom de variante", blank=True, null=True)
    image = models.ImageField(upload_to='shop', blank=True, null=True)
    option_name_1 = models.ForeignKey(OptionName, on_delete=models.CASCADE, verbose_name="Nom de l'option 1", blank=True, null=True, related_name='option_name_1_variants')
    option_1 = models.CharField(max_length=255, verbose_name="Option 1", blank=True, null=True)
    option_name_2 = models.ForeignKey(OptionName, on_delete=models.CASCADE, verbose_name="Nom de l'option 2", blank=True, null=True, related_name='option_name_2_variants')
    option_2 = models.CharField(max_length=255, verbose_name="Option 2", blank=True, null=True)
    stock = models.IntegerField(default=0, verbose_name="Stock")
    price = models.DecimalField(max_digits=7, decimal_places=2, default = 0.00,verbose_name="Prix")
    
    class Meta:
        verbose_name = "Variante"
    
        
    def __str__(self) -> str:
        return f"{self.product.product_title} - {self.variant_name}"
    
    @property    
    def product_variant_title(self):
        return f"{self.product.name} - {self.variant_name}"
    
    def save(self, *args, **kwargs):
        variant_name = ""
        if self.option_1:
            variant_name += f"{self.option_1} - "
        if self.option_2:
            variant_name += f"{self.option_2}"
        variant_name = variant_name.rstrip().rstrip('-')
        self.variant_name = variant_name 
        if not self.variant_slug:
            self.variant_slug = slugify(self.variant_name)  
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    products = models.ManyToManyField(Product, through='CartProduct')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_product = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Panier"
    
    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return f"Anonymous cart ({self.session_key})"
           
        
     # Calculate the total amount of the cart
    @property
    def calculate_total(self):
        cart_products = self.cartproduct_set.all()
        total = sum([cp.quantity * cp.product_variant.price for cp in cart_products if cp.selected == True])
        self.total = total
        self.save()
        return total
    
    @property
    def calculate_quantity(self):
        # Calculate the total quantity of the cart
        cart_products = self.cartproduct_set.all()
        quantity = sum([cp.quantity for cp in cart_products if cp.selected == True])
        self.total_product = quantity
        return quantity
    
    def remove_cart_product(self, cart, product, product_variant):
        cart_product = get_object_or_404(CartProduct, cart=cart, product=product, product_variant=product_variant)
        cart_product.delete()
        
    def add_product(self, cart, product, product_varitant, quantity):
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            product_variant=product_varitant,
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        else:
            cart_product.quantity = quantity
            cart_product.save()

    def create_order(self):
        order = Order.objects.create(user=self.user, total=self.total, quantity=self.total_product)

        for cart_product in self.cartproduct_set.filter(selected=True):
            order_product = OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)

        return order
        

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_cart_product(self):
        return self.product_variant.price * self.quantity
    
    @property
    def cart_product_title(self):
        return f"{self.product.product_title} - {self.product_variant.variant_name}"
    
class Order(models.Model):
    # Fields for Order model
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('canceled', 'Canceled')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'

class OrderProduct(models.Model):
    # Fields for OrderProduct model
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Avis")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    verified_purchase = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.user.first_name}"

    class Meta:
        verbose_name = "Avis"
        unique_together = ('user', 'product')