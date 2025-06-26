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
    path('refunds/', views.refund_page, name='refund_page'),     
    path('utensils/', views.utensils, name='utensils'),
    path('products/', views.product_list, name='product_list'),
    path('privacy/',views.privacy,name='privacy'),
    path('about/', views.about,name='about'),
    path('faq/',views.faq, name='faq'),
    path('security/',views.security, name='security'),
    path('service/',views.service, name='service'),
    path('shipping/', views.shipping, name='shipping'),
    path('contact', views.contact, name='contact'),
    path('helpCenter/',views.helpCenter, name='helpCenter'),


]

