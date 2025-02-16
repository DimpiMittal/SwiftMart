from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product 

# Index view (Homepage)
def index(request):
    return render(request, 'store/index.html')

# Shop page view
def shop_view(request):
    return render(request, 'store/shop.html')

# Cart page view
def cart_view(request):
    return render(request, 'store/cart.html')

# Profile page view (only for logged-in users)
@login_required
def profile_view(request):
    return render(request, 'store/profile.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile page after successful login
        else:
            # Add error message if login fails
            error_message = "Invalid credentials"
            return render(request, 'store/login.html', {'error_message': error_message})
    
    return render(request, 'store/login.html')

# Registration view (sign up)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile page after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'store/register.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to homepage after logout


from .models import WomenProduct

def women_style(request):
    products = WomenProduct.objects.all()  # Fetching all products from the WomenProduct table
    return render(request, 'store/women-style.html', {'products': products})

from .models import MenProduct

def men_style(request):
    products = MenProduct.objects.all()  # Fetching all products from the MenProduct table
    return render(request, 'store/men-style.html', {'products': products})


from .models import KidsProduct

def kids_style(request):
    products = KidsProduct.objects.all()  # Fetching all products from the KidsProduct table
    return render(request, 'store/kids-style.html', {'products': products})

from .models import NewProduct

def new_style(request):
    products = NewProduct.objects.all()  # Fetching all products from the NewProduct table
    return render(request, 'store/new-style.html', {'products': products})


from .models import UtensilsProduct

def utensils(request):
    products = UtensilsProduct.objects.all()  # Fetching all products from the UtensilsProduct table
    return render(request, 'store/utensils.html', {'products': products})



def product_list(request):
    # Fetching products from all categories
    all_products = WomenProduct.objects.all() | MenProduct.objects.all() | KidsProduct.objects.all() | NewProduct.objects.all() | UtensilsProduct.objects.all()
    return render(request, 'store/product_list.html', {'products': all_products})
