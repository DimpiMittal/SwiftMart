from django.urls import path
from .views import (
    register_view,verify_otp_view, login_view, logout_view, profile_view, 
    update_profile, index_view, send_login_otp, verify_login_otp, 
    send_reset_otp, verify_reset_otp
)

urlpatterns = [
    # Home Page
    path('', index_view, name='index'),

    # User Authentication
    path('register/', register_view, name='register'),
   path('verify-otp/', verify_otp_view, name='verify_otp'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # User Profile
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),

    # OTP-Based Login System
    path('otp/login/send/', send_login_otp, name='send_login_otp'),
    path('otp/login/verify/', verify_login_otp, name='verify_login_otp'),

    # OTP-Based Password Reset
    path('otp/reset/send/', send_reset_otp, name='send_reset_otp'),
    path('otp/reset/verify/', verify_reset_otp, name='verify_reset_otp'),
]
