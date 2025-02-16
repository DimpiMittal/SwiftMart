from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/', views.cart_view, name='cart'),
    path('profile/', views.profile_view, name='profile'),
    path('women-style/', views.women_style, name='women-style'), 
    path('men-style/', views.men_style, name='men-style'),        
    path('kids-style/', views.kids_style, name='kids-style'),     
    path('new-style/', views.new_style, name='new-style'),        
    path('utensils/', views.utensils, name='utensils'),
     path('products/', views.product_list, name='product_list'),
]

