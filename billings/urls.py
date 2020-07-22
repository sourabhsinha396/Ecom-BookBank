from django.urls import path
from .views import checkout_address_create_view,checkout_address_reuse_view
app_name = 'billings'
urlpatterns = [
    #############--------Function Based------###############
    path('checkout/address-create/',checkout_address_create_view,name="checkout_address_create_view"),
    path('checkout/address-reuse/',checkout_address_reuse_view,name="checkout_address_reuse_view"),
    ]
