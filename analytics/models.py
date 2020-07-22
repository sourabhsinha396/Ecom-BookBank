from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#from this module
from .utils import get_client_ip
from .signals import object_viewed_signal

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    user          = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)
    ip_address    = models.CharField(max_length=100,blank=True,null=True)
    content_type  = models.ForeignKey(ContentType,on_delete = models.SET_NULL,null=True,blank=True) #Product,Order,Cart etc
    object_id     = models.PositiveIntegerField() #product_id,order_id etc
    content_object= GenericForeignKey('content_type','object_id')
    timestamp     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

    def __str__(self):
        return "%s viewed %s" %(self.user,self.content_object)

def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    print(sender)
    user = request.user if request.user.is_authenticated else None
    new_view_obj = ObjectViewed.objects.create(
    user      = user,
    object_id = instance.id,
    ip_address= get_client_ip(request),
    content_type = ContentType.objects.get_for_model(sender) #same as instance.__class__
    )


object_viewed_signal.connect(object_viewed_receiver)
