from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import SignUpForm, LoginForm
from .models import CustomUser

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
        response = super().form_valid(form)
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(1209600) # expire in 2 weeks
        return response
    
class Logout(LogoutView):
    next_page = 'shop:home_shop'
    
def profile(request):
    
    return render(request, "profile.html", context={
        
    })