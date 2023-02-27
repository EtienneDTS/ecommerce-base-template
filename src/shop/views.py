from django.shortcuts import render, get_object_or_404, redirect


from .models import Product, Cart, CartProduct

# Create your views here.

def home_view(request):
    products = Product.objects.all()
    return render(request, "shop/home_shop.html", context={
        "products": products,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", context={
        "product": product,
    })
    
def add_to_cart(request, slug):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if request.user.is_authenticated:
            user=request.user
        else:
            #Retrieve the user's hash while waiting for them to log in.
            user=request.session.get('_auth_user_hash')

        product = get_object_or_404(Product, slug=slug)
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        else:
            cart_product.quantity = quantity
            cart_product.save()
    return redirect('shop:cart')

def cart(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        #Retrieve the user's hash while waiting for them to log in.
        user=request.session.get('_auth_user_hash')
    cart = get_object_or_404(Cart, user=user)
    cart_products = cart.cartproduct_set.all()
    # Update products quantity in cart.
    if request.method == 'POST':
        for cart_product in cart_products:
            new_quantity = int(request.POST.get("quantity"))
            if new_quantity > 0:
                cart_product.quantity = new_quantity
                cart_product.save()
            else:
                cart.remove_cartproduct(cart_product.product)
                return redirect('shop:cart')
    return render(request, "shop/cart.html", context={
        "cart_product": cart_products,
    })
    
def remove_from_cart(request, slug):
    if request.user.is_authenticated:
        user=request.user
    else:
        #Retrieve the user's hash while waiting for them to log in.
        user=request.session.get('_auth_user_hash')
    product = get_object_or_404(Product, slug=slug)
    cart = get_object_or_404(Cart, user=user)
    cart.remove_cartproduct(product)
    return redirect('shop:cart')