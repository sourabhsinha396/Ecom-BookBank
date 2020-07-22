from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

#from others module
from user_auth.models import GuestEmail

User  = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            obj,created = self.model.objects.get_or_create(user = user,email = user.email)
        elif guest_email_id is not None:
            '''We are deleting guest_email_id after login,so if its present user is definetely a guest'''
            guest_email_obj = GuestEmail.objects.get(id = guest_email_id)
            obj,created     = self.model.objects.get_or_create(email = guest_email_obj.email)
        else:
            print("Else ran in billing models")
        return obj,created



class BillingProfile(models.Model):
    user  = models.OneToOneField(User,unique=True,on_delete = models.CASCADE,null=True,blank=True) # to allow guest user blank,null
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()
    def __str__(self):
        return str(self.user)+str(self.id)

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_receiver,sender=User)

##------------------ Address Model --------------------------------------------

ADDRESS_TYPE = (
('billing','Billing'),
('shipping','Shipping'),
)
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=60,default="billing",choices = ADDRESS_TYPE)
    address_line_1   = models.CharField(max_length=60)
    address_line_2   = models.CharField(max_length=60,blank=True,null=True)
    city            = models.CharField(max_length=60)
    state           = models.CharField(max_length=60)
    postal_code     = models.CharField(max_length=60)
    country         = models.CharField(max_length=60,default="India")
    phone_no        = models.CharField(max_length=60)

    def __str__(self):
        return str(self.id)

    def get_address(self):
        return "{line1},{line2}<br>{city}".format(
        line1 = self.address_line_1,
        line2 = self.address_line_2 or " ", #so as to not display none
        city= self.city)
