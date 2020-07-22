from django.shortcuts import render,redirect
from django.http import JsonResponse
# from django.core import serializers

# from other folders
from products.models import Product
from orders.models import Order
from user_auth.forms import LoginForm,GuestForm
from user_auth.models import GuestEmail
from billings.models import BillingProfile,Address
from billings.forms import AddressForm
#from this folder
from .models import Cart

def cart_home(request):
    '''Logic to allow logged in + guest users to add items to cart,
    When we log in it doesn't clean out the old session'''
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    context={'cart':cart_obj}
    return render(request,'carts/cart_home.html',context)



def cart_update(request,id):
    product_obj = Product.objects.get(id=id)
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        added = False
    else:
        cart_obj.products.add(product_obj) # we can also pass id instead of product_obj
        added = True
    cart_obj_count = cart_obj.products.count()
    request.session['cart_total_items'] = cart_obj_count
    if request.is_ajax():
        json_data = {
        'added':added,
        'cart_item_count':cart_obj_count
        }
        return JsonResponse(json_data)
    return redirect("cart:func_cart_home")

def checkout_home(request):
    context = {}
    order_obj = None
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if new_obj or cart_obj.products.count() == 0:
        return redirect("cart:func_cart_home")

    user = request.user
    billing_profile = None
    address_qs      = None

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id')
    billing_address_id = request.session.get('billing_address_id')

    print("yo",shipping_address_id,billing_address_id)

    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile,new_billing_profile = BillingProfile.objects.get_or_create(user=user,email = user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id = guest_email_id)
        billing_profile,billing_guest_profile_created = BillingProfile.objects.get_or_create(email = guest_email_obj.email)
    print(billing_profile)
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs              = Address.objects.filter(billing_profile=billing_profile)[:5]

        order_obj,new_order_obj = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id = shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address  = Address.objects.get(id = billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()


    if request.method=="POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_item_count'] = 0
            del request.session['cart_id']
            return redirect("/cart/success")
    context = {'object':order_obj,'billing_profile':billing_profile,'form':login_form,'guest_form':guest_form,
                'address_form':address_form,'billing_address_form':billing_address_form,
                'address_qs':address_qs}
    return render(request,'carts/checkout.html',context)



def checkout_done_view(request,id):
    order_obj = Order.objects.get(id = id)
    context = {'object':order_obj}
    return render(request,'carts/checkout_done.html',context)
