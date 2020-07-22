from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,m2m_changed
# custom apps imports
from products.models import Product
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get('cart_id')
        qs = self.get_queryset().filter(id = cart_id)
        if qs.count() == 1:
            new_obj  = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj  = Cart.objects.new_cart(user = request.user)
            new_obj   = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj,new_obj

    def new_cart(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User,on_delete = models.CASCADE,null=True,blank=True) #any user can create a cart,even unauthenticated
    products    = models.ManyToManyField(Product,blank=True)
    subtotal    = models.DecimalField(default=0.00,max_digits=9,decimal_places=2)
    total       = models.DecimalField(default=0.01,max_digits=9,decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.user)+str(self.id)

def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    '''Product and Cart are related by ManyToManyField ,pre_save was not working correctly'''
    print(action)
    if action=="post_add" or action =="post_remove" or action=="post_clear":
        products = instance.products.all()
        newsubtotal = 0
        for x in products:
            newsubtotal += x.price
        if instance.subtotal != newsubtotal:
            instance.subtotal = newsubtotal
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    instance.total = instance.subtotal #* decimal.Decimal(1.2)   # 1.2 to replicate tax,shipping charges

pre_save.connect(pre_save_cart_receiver,sender=Cart)
