from django.shortcuts import render, redirect

from .forms import SignUpForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:home_shop')
    else:
        form = SignUpForm()
    return render(request, "signup.html", context={
        "form": form
    })