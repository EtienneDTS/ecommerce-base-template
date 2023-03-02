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
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            if not request.session.session_key:
                request.session.save()
            #Retrieve the user's session_key while waiting for them to log in.
            session_key = request.session.session_key or request.session.cycle_key()
            if session_key == None:
                request.session.cycle_key()
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        product = get_object_or_404(Product, slug=slug)    
        cart.add_product(cart, product, quantity)
    return redirect('shop:cart')

def cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        #Retrieve the user's session_key while waiting for them to log in.
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        
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
        "cart_products": cart_products,
    })
    
def remove_from_cart(request, slug):
    if request.user.is_authenticated:
        user=request.user
        cart = get_object_or_404(Cart, user=user)
    else:
        #Retrieve the user's hash while waiting for them to log in.
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        
    product = get_object_or_404(Product, slug=slug)
    cart.remove_cartproduct(product)
    return redirect('shop:cart')