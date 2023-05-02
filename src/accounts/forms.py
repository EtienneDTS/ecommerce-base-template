import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
        ]
        
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['email'].label_suffix = ""
            self.fields['first_name'].label_suffix = ""
            self.fields['last_name'].label_suffix = ""
            self.fields['password'].label_suffix = ""
            self.fields['confirm_password'].label_suffix = ""
    
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
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if not first_name or not last_name:
            raise forms.ValidationError("Veuillez inscrire votre prénom et votre nom de famille.")
    
class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label="Se souvenir de moi",
        label_suffix=""
        
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "e-mail"
        self.fields['username'].label_suffix = ""
        self.fields['password'].label = "Mot de passe"
        self.fields['password'].label_suffix = ""
        
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        print(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        if len(password2) < 8:
            raise ValidationError("Le mot de passe doit comporter au moins 8 caractères.")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,}$', password2):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre, une lettre majuscule, une lettre minuscule, un caractère spécial et avoir une longueur minimale de 8 caractères.")
        return password2