from django.urls import path
from .views import (cart_home,cart_update,
                    checkout_home,checkout_done_view)

app_name = 'cart'
urlpatterns = [
    #############--------Function Based------###############
    path('cart/',cart_home,name="func_cart_home"),
    path('update-cart/<int:id>/',cart_update,name="func_cart_update"),
    path('checkout/',checkout_home,name="checkout"),
    path('checkout-done/<int:id>/',checkout_done_view,name="checkout_done"),
    ]
