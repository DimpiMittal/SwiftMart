from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

import random
import time

from .forms import CustomUserCreationForm
from .models import Profile

# Store OTPs temporarily (valid for 45 seconds)
otp_storage = {}

# Helper function to generate and send OTP
def generate_and_send_otp(email, subject):
    otp = random.randint(1000, 9999)  # 4-digit OTP
    otp_storage[email] = {'otp': otp, 'timestamp': time.time()}
    
    send_mail(
        subject,
        f'Your OTP is {otp}. It is valid for 45 seconds.',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return otp

# Helper function to validate OTP (45-sec limit)
def validate_otp(email, otp_entered):
    if email in otp_storage:
        stored_otp = otp_storage[email]['otp']
        if time.time() - otp_storage[email]['timestamp'] > 45:  # OTP expired
            del otp_storage[email]  # Remove expired OTP
            return False
        del otp_storage[email]  # Remove OTP after successful use
        return int(otp_entered) == stored_otp
    return False

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            messages.success(request, "Registration successful! Welcome to SwiftMart.")
            return redirect('profile')  # Redirect to profile page after signup
        else:
            messages.error(request, "There was an error in the form. Please try again.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('login')

        # Authenticate using username (not email)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('profile')  # Ensure 'profile' URL is named correctly
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')  # Stay on login page if invalid

    return render(request, 'accounts/login.html') 


def send_login_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            request.session['login_email'] = email
            generate_and_send_otp(email, 'Your OTP for Login')
            messages.info(request, 'An OTP has been sent to your email.')
            return render(request, 'accounts/login.html', {'page': 'verify_login_otp', 'email': email})
        messages.info(request, 'User with this email does not exist.')
    return render(request, 'accounts/login.html', {'page': 'login'})

def verify_login_otp(request):
    if request.method == 'POST':
        email = request.session.get('login_email')
        otp_entered = request.POST.get('otp')

        if not email:
            messages.error(request, 'Session expired. Please request a new OTP.')
            return redirect('login')

        if validate_otp(email, otp_entered):
            user = User.objects.get(email=email)
            login(request, user)
            del request.session['login_email']
            messages.success(request, 'Login successful!')
            return redirect('profile')

        messages.error(request, 'Invalid or expired OTP.')
        return redirect('send_login_otp')

    return render(request, 'accounts/login.html', {'page': 'verify_login_otp'})


# Send Password Reset OTP
def send_reset_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            request.session['reset_email'] = email
            generate_and_send_otp(email, 'Your OTP for Password Reset')
            messages.info(request, 'An OTP has been sent to reset your password.')
            return render(request, 'accounts/login.html', {'page': 'verify_reset_otp', 'email': email})
        messages.error(request, 'User with this email does not exist.')
    return render(request, 'accounts/login.html', {'page': 'reset_password'})

# Verify Reset OTP
def verify_reset_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')

        if validate_otp(email, otp_entered):
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password and new_password == confirm_password:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful!')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Invalid or expired OTP.')
    
    return render(request, 'accounts/login.html', {'page': 'verify_reset_otp'})

# Profile View
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

# Profile Update View
@login_required
def update_profile(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect("profile")
    return render(request, "accounts/profile.html")

# Home Page
def index_view(request):
    return render(request, 'store/index.html')


# Verify Registration OTP
def verify_otp_view(request):
    if request.method == 'POST':
        email = request.session.get('pending_user', {}).get('email')
        otp_entered = request.POST.get('otp')

        if validate_otp(email, otp_entered):
            user_data = request.session.pop('pending_user', None)
            if user_data:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                login(request, user)
                send_mail(
                    'Registration Successful',
                    'You have successfully registered!',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Registration successful!')
                return redirect('profile')

        messages.error(request, 'Invalid or expired OTP.')
        return redirect('register')

    return redirect('register')