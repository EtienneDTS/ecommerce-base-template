from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


from .models import Product, Cart, CartProduct, Review
from .forms import ReviewForm

# Create your views here.

def home_view(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    return render(request, "shop/home_shop.html", context={
        "products": products,
        "cart": cart,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    return render(request, "shop/product_detail.html", context={
        "product": product,
        "cart": cart,
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
            product_id = request.POST.get("product_id")
            new_quantity = int(request.POST.get(f"quantity_{product_id}"))
            if cart_product.id == int(product_id):
                if new_quantity > 0:
                    cart_product.quantity = new_quantity
                    cart_product.save()
                else:
                    cart.remove_cart_product(cart_product.product)
                    return redirect('shop:cart')
    return render(request, "shop/cart.html", context={
        "cart_products": cart_products,
        "cart": cart
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
    cart.remove_cart_product(product)
    return redirect('shop:cart')


def update_selected_status(request):
    if request.method == 'POST':
        cart_product_id = request.POST.get('cart_product_id')
        selected = request.POST.get('selected') == 'true'
        cart_product = get_object_or_404(CartProduct, id=cart_product_id)
        cart_product.selected = selected
        cart_product.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
    
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    review = Review.objects.filter(product=product, user=request.user).first()
    form = ReviewForm(request.POST)

    if request.method == 'POST':
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        return redirect('shop:product_detail', slug=slug)

    context = {
        'product': product,
        'form': form,
        'review': review,
    }

    return render(request, 'product_review/add_review.html', context)