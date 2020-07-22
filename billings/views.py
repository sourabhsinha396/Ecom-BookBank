from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

# from this app
from .forms import AddressForm
from .models import BillingProfile,Address
# Create your views here.
def checkout_address_create_view(request):
    if request.method == "POST":
        form  = AddressForm(request.POST)
        next_ = request.GET.get('next')
        next_post =request.POST.get('next')
        redirect_path= next_ or next_post
        if form.is_valid():
            print(request.POST)
            instance = form.save(commit=False)
            billing_profile,new_billing = BillingProfile.objects.new_or_get(request)
            print(billing_profile)
            if billing_profile is not None:
                instance.billing_profile = billing_profile
                address_type             = request.POST.get('address_type','shipping')
                instance.address_type    = address_type
                instance.save()
                request.session[address_type+'_address_id'] = instance.id
            else:
                print("error in checkout_address_create_view else")
                return redirect("cart:func_cart_home")
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("cart:checkout")
    else:
        return redirect("cart:func_cart_home")

def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            next_ = request.GET.get('next')
            next_post =request.POST.get('next')
            redirect_path= next_ or next_post
            address_id = request.POST.get('shipping_address')

            print(request.POST)
            billing_profile,new_billing = BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                if address_id:
                    qs = Address.objects.filter(billing_profile = billing_profile,id = address_id)
                    if qs.exists():
                        address_type             = request.POST.get('address_type','shipping')
                        request.session[address_type+'_address_id'] = address_id
            else:
                print("error in checkout_address_create_view else")
                return redirect("cart:func_cart_home")
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
        else:
            return redirect("cart:func_cart_home")
