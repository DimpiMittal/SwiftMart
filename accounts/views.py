from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm  # Custom user creation form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required

# Register View
def register_view(request):
    """
    Handles user registration. Automatically logs in the user after successful registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

# Login View
def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the user
            messages.success(request, 'You are now logged in!')
            return redirect('profile')  # Redirect to profile page after login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Profile View
@login_required
def profile_view(request):
    """
    Displays the profile page for logged-in users.
    """
    return render(request, 'accounts/profile.html')

# Logout View
def logout_view(request):
    """
    Handles user logout and redirects to the index page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')  # Redirect to the index page after logout

# Index View
def index_view(request):
    """
    Displays the home page.
    """
    return render(request, 'store/index.html')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile 

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user  # Get the logged-in user
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Update user details
        user.email = email
        user.save()

        # Update profile details (assuming Profile model exists)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.address = address
        profile.save()

        return redirect("profile")  # Redirect to the profile page after saving
    
    return render(request, "profile.html")
