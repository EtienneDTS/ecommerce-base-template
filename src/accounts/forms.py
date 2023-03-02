import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]
        
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    #all clean_data transleted in french   
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée. Veuillez utiliser une adresse email différente.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("Le mot de passe doit comporter au moins 8 caractères.")
        if not re.match(r'[A-Za-z0-9@#$%^&+=]+', password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins un chiffre, une lettre majuscule, une lettre minuscule, un caractère spécial et avoir une longueur minimale de 8 caractères.")
        return password
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas. Veuillez saisir le même mot de passe dans les deux champs.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, des chiffres et des underscores.")
        return username
    
class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label="Remember me"
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Adresse e-mail"
        self.fields['password'].label = "Mot de passe"