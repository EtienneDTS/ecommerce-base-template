from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


from .models import Product, Cart, CartProduct, Review, ProductVariant
from .forms import ReviewForm

# Create your views here.

def home_view(request):
    products_variant = ProductVariant.objects.all().order_by('price')
    product_list=[]
    first_price_variant_per_products = []
    for product_variant in products_variant:
        if product_variant.product not in product_list:
            first_price_variant_per_products.append(product_variant)
            product_list.append(product_variant.product)
            
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    return render(request, "shop/home_shop.html", context={
        "first_price_variant_per_products": first_price_variant_per_products,
        "cart": cart,
        "products_variant": products_variant,
    })

def product_detail(request, slug, variant_slug):
    print("bonjour")
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        color = request.POST.get("color")
        flavor = request.POST.get("flavor")
        option = request.POST.get("option")
        if flavor != None:
            product_variant = get_object_or_404(ProductVariant, product=product, flavor=flavor, option=option)
        if color != None:
            product_variant = get_object_or_404(ProductVariant, product=product, color=color, option=option)
        options = product_variant.get_options_for_product_variant()
    else :
        product_variant = get_object_or_404(ProductVariant, variant_slug=variant_slug)
        print("else")
    print(product_variant)
    product_variants = ProductVariant.objects.filter(product=product).order_by("price")
    flavors = set([variant.flavor for variant in product_variants if variant.flavor])
    colors = set([variant.color for variant in product_variants if variant.color])
    options = product_variant.get_options_for_product_variant()
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    
    context={
        "product": product,
        "cart": cart,
        "product_variants": product_variants,
        "product_variant": product_variant,
        "flavors": flavors,
        "options": options,
        "colors": colors,
        "option_name": product_variant.option_name,
    } 
    
        
    return render(request, "shop/product_detail.html", context)

def product_detail_with_option(request, slug, variant_slug):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    
    if request.method == "POST":
        
        product = get_object_or_404(Product, slug=slug)
        product_variants = ProductVariant.objects.filter(product=product).order_by("price")
        flavors = set([variant.flavor for variant in product_variants if variant.flavor])
        colors = set([variant.color for variant in product_variants if variant.color])
        color = request.POST.get("color")
        flavor = request.POST.get("flavor")
        option = request.POST.get("option")
        if flavor != None:
            product_variant = get_object_or_404(ProductVariant, product=product, flavor=flavor, option=option)
        if color != None:
            product_variant = get_object_or_404(ProductVariant, product=product, color=color, option=option)
        options = product_variant.get_options_for_product_variant()
        

        context={
            "product": product,
            "cart": cart,
            "product_variants": product_variants,
            "product_variant": product_variant,
            "flavors": flavors,
            "options": options,
            "colors": colors,
            "option_name": product_variant.option_name,
            "price": product_variant.price
        } 
        return render(request, "shop/product_detail.html", context)

    
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