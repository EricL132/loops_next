from django.urls import path
from .views import *

urlpatterns = [
    path('products',GetProducts.as_view()),
    path('men',GetMensProducts.as_view()),
    path('women',GetWomensProducts.as_view()),
    path('kids',GetKidsProducts.as_view()),
    path('product',GetProduct.as_view()),
    path('feature',GetFeatured.as_view()),
    path('register',Register.as_view()),
    path('login',Login.as_view()),
    path('forgot',Forgot.as_view()),
    path('reset/<slug:token>',Reset.as_view()),
    path('account',GetAccountInfo.as_view()),
    path('logout',LogOut.as_view()),
    path('info',GetInfo.as_view()),
    path('search/',SearchItem.as_view()),
    path('coupon/',CheckCoupon.as_view()),
    path('stock',CheckStock.as_view()),
    path('createorder',CreateOrder.as_view()),
    path('checkout/<slug:order>/capture/',CaptureOrder.as_view()),
    path('order/<slug:order>',GetOrderInfo.as_view()),
]
