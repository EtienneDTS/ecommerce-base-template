from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import SignUpForm, LoginForm, CustomPasswordChangeForm
from .models import CustomUser
from shop.models import Cart

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            password = cleaned_data.pop('password')
            confirm_password = cleaned_data.pop('confirm_password')
            # Créer l'utilisateur avec un mot de passe crypté
            if password == confirm_password:
                user = CustomUser(**cleaned_data)
                user.set_password(password)
                user.save()
                return redirect('shop:home_shop')
            else:
                form.add_error('confirm_password', "Les mots de passe ne correspondent pas.")
    else:
        form = SignUpForm()
    return render(request, "signup.html", context={
        "form": form
    })
    
class Login(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('shop:home_shop')
    authentication_form = LoginForm
    fields = ['email', 'password']

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        session_key=self.request.session.session_key
        print(session_key)
        response = super().form_valid(form)
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(86400) # expire in 24 hours
        
        # Keep the user's cart after login
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key).first()
            user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
            if session_cart and session_cart.cartproduct_set.count() > 0:
                for cart_product in session_cart.cartproduct_set.all():
                    product = cart_product.product
                    product_variant = cart_product.product_variant
                    quantity = cart_product.quantity
                    user_cart.add_product(user_cart, product, product_variant, quantity)
                session_cart.delete()
        return response
    
class Logout(LogoutView):
    next_page = 'shop:home_shop'
    
def profile(request):
    
    return render(request, "profile.html", context={
        
    })
    
    
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("form valid")
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été modifié avec succès !')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})