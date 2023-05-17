from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Max


from .models import Product, Cart, CartProduct, Review, ProductVariant
from .forms import ReviewForm

# Create your views here.
def home_view(request, category):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user.id).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    products_variant_list = ProductVariant.objects.all()
    min_price = request.GET.get("input_min")
    max_price = request.GET.get("input_max")
    sort_by = request.GET.get("sort_by")
    if min_price == None or max_price == None:
        min_price = "0"
        max_price = 0
        sort_by = "none"
    # filtrage par catégorie
    if category != "all":
        products_variant_list = products_variant_list.filter(product__categories__name=category)
    else:
        category = "TOUS NOS PRODUITS"
    # filtrage par fourchette de prix
    max_variant_price = products_variant_list.aggregate(Max('price'))['price__max']
    if max_price != 0:
        products_variant_list = products_variant_list.filter(price__gte=min_price, price__lte=max_price)
    else :
        max_price = max_variant_price

    # tri par prix croissant ou décroissant
    if sort_by == "asc_price":
        products_variant_list = products_variant_list.order_by("price")
    if sort_by == "desc_price":
        products_variant_list = products_variant_list.order_by("-price")  
    if sort_by == "a-z":
        products_variant_list = products_variant_list.order_by('product__brand', 'product__name')
    if sort_by == "z-a":
        products_variant_list = products_variant_list.order_by('-product__brand', '-product__name')
    products_variant_list_count = products_variant_list.count() 
    max_price = str(max_price)
    min_price = str(min_price)
    max_variant_price = str(max_variant_price)
    try:
        cart_products = cart.cartproduct_set.all()
    except:
        cart_products = []
    
    context = {
        "sort_by": sort_by,
        "category": category,
        "products_variant_list_count": products_variant_list_count,
        "min_price": min_price,
        "max_price": max_price,
        "cart": cart,
        "cart_products": cart_products,
        "products_variant_list": products_variant_list,
        "max_variant_price": max_variant_price,
    }
    return render(request, "shop/home_shop.html", context
    )


def product_detail(request, slug, variant_slug, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    product_variants = ProductVariant.objects.filter(product=product).order_by("price")
    product_variant = get_object_or_404(ProductVariant, variant_slug=variant_slug, product=product, id=variant_id)
    options_1 = set([variant.option_1 for variant in product_variants if variant.option_1])
    if product_variant.option_1 :
        options_2 = set([variant.option_2 for variant in product_variants.filter(option_1=product_variant.option_1) if variant.option_2])
    else:
        options_2 = set([variant.option_2 for variant in product_variants if variant.option_2])
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    context={
        "product": product,
        "cart": cart,
        "product_variants": product_variants,
        "product_variant": product_variant,
        "options_1": options_1,
        "options_2": options_2,
        "option_name_1": product_variant.option_name_1,
        "option_name_2": product_variant.option_name_2,
    } 
    
    return render(request, "shop/product_detail.html", context)

    
def get_product_variant_url(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print("salut salut salut")
    if request.method == "POST":
        if request.POST.get("option_1") != None:    
            option_1 = request.POST.get("option_1")
            product_variant = ProductVariant.objects.filter(product=product, option_1=option_1).order_by("price").first()
            url = reverse('shop:product_detail', args=[product.slug, product_variant.variant_slug, product.id, product_variant.id ])
            data = {'url': url} 
        return JsonResponse(data)
    
def update_variant_detail(request, product_id):
    print("bonjour")
    product = get_object_or_404(Product, id=product_id)
    option_1 = None
    if request.method == "POST":
        if request.POST.get("option_1") != None:    
            option_1 = request.POST.get("option_1")
        if request.POST.get("option") != None:
            option = request.POST.get("option")
        product_variant = get_object_or_404(ProductVariant, product=product, option_2=option, option_1=option_1)
        data = {
            "image_url": product_variant.image.url,
            "price": product_variant.price,
            "variant_id": product_variant.id,
            }   
        return JsonResponse(data)
        
def add_to_cart(request, product_id):
    if request.method == 'POST':
        variant_id = request.POST.get("variant_id")
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
        product = get_object_or_404(Product, id=product_id)
        product_variant = get_object_or_404(ProductVariant, product=product, id=variant_id)    
        cart.add_product(cart, product, product_variant, quantity)
        new_cart_quantity = cart.calculate_quantity
        data = {'success': True, 'new_cart_quantity': new_cart_quantity}
    return JsonResponse(data)


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
                    cart.remove_cart_product(
                        cart=cart, product=cart_product.product, product_variant=cart_product.product_variant)
    request.session['cart_quantity'] = cart.calculate_quantity
    return render(request, "shop/cart.html", context={
        "cart_products": cart_products,
        "cart": cart,
    })
    
def remove_from_cart(request, product_id, variant_id):
    if request.user.is_authenticated:
        user=request.user
        cart = get_object_or_404(Cart, user=user)
    else:
        #Retrieve the user's hash while waiting for them to log in.
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        
    product = get_object_or_404(Product, id=product_id)
    product_variant = get_object_or_404(ProductVariant, product=product, id=variant_id)
    cart.remove_cart_product(cart=cart, product=product, product_variant=product_variant)
    return redirect("shop:cart")

def remove_from_cart_dropdown(request, cart_product_id): 
    if request.user.is_authenticated:
        user=request.user
        cart = get_object_or_404(Cart, user=user)
    else:
        #Retrieve the user's hash while waiting for them to log in.
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, _ = Cart.objects.get_or_create(session_key=session_key)  
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    print(cart_product)
    cart_product.delete()
    total_quantity = cart.calculate_quantity
    return JsonResponse({'success': True, "total_quantity":total_quantity})

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

def get_cart_data(request):
    if request.user.is_authenticated:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    
    products_data = []
    cart_products = cart.cartproduct_set.all()
    for cart_product in cart_products:
        product_detail_url = reverse(
        'shop:product_detail', 
        kwargs={'slug': cart_product.product.slug,
                'variant_slug': cart_product.product_variant.variant_slug,
                'product_id': cart_product.product.id,
                'variant_id': cart_product.product_variant.id,
        })
        data = {
            "name": cart_product.cart_product_title,
            "price": cart_product.total_cart_product,
            "image": cart_product.product_variant.image.url,
            "quantity": cart_product.quantity,
            "id": cart_product.id,
            "url": product_detail_url,
        }
        products_data.append(data)
    
    cart_total_quantity = cart.calculate_quantity
    cart_total_ttc = cart.calculate_total
    
    cart_data = {
        "products": products_data,
        "total_quantity": cart_total_quantity,
        "total_ttc": cart_total_ttc,
    }
    return JsonResponse(cart_data)
