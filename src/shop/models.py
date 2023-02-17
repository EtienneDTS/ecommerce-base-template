from django.db import models
from django.db import models

from accounts.models import CustomUser
# Create your models here.


    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self) -> str:
        return f"Cart for {self.user.username}"
    
    def calculate_total(self):
        cart_products = self.cartproduct_set.all()
        total = sum([cp.quantity * cp.product.price for cp in cart_products])
        self.total = total
        self.save()
        return total
    
    def calculate_quantity(self):
        cart_products = self.cartproduct_set.all()
        quantity = sum([cp.quantity for cp in cart_products])
        return quantity

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class Order(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)