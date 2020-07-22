import os
import random
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

# Third Party Imports
from taggit.managers import TaggableManager


# Imports from this folder
from .utils import unique_slug_generator


def get_filename_extension(filepath):
    '''This gives the extension of our filename e.g. fo water.jpg it will return "water" and "jpg" '''
    base_name = os.path.basename(filepath)
    name,extension  = os.path.splitext(base_name)
    return name,extension

def upload_image_path(instance,filename):
    new_filename = random.randint(1,347983479)
    name,extension = get_filename_extension(filename)
    final_filename = '{new_filename}{extension}'.format(new_filename=new_filename,extension=extension)
    return "book_images/{final_filename}".format(final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def get_active(self): # This Filters down the results to have only active products
        return self.filter(is_active=True)


class ProductManager(models.Manager):
    def get_queryset(self):  # I over-rided get_queryset to have products which is active and is ready to be shown
        return ProductQuerySet(self.model,using = self._db)

    def all(self): #We can over-ride the default Product.objects.all() function
        return self.get_queryset() #.get_active()

    def active_only(self):
        return self.get_queryset().get_active()

    def get_million_copies_book(self):
        '''get_queryset gets an addon that it can now access ProductQuerySet's Functions,
        its not that get_queryset is passing through what is being returned by ProductQuerySet
        self.get_queryset().filter(title__icontains = "Million") will still return un-active ones also'''
        qs = self.get_queryset().get_active().filter(title__icontains = "Million")
        return qs # To use this function using in views-. 'Product.objects.get_million_copies_book()'

class Product(models.Model):
    title       = models.CharField(max_length = 100)
    slug        = models.SlugField(blank=True,unique=True) #we allowed blank=True to use signal and generate slug before saving
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=5)
    image       = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    tags        = TaggableManager()
    is_active   = models.BooleanField(default=False)

    objects = ProductManager()
    def __str__(self):
        return str(self.title)[:20]

    def get_absolute_url(self):
        return reverse("products:func_product_detail_by_slug",kwargs={'slug':self.slug})
        # reverse is more consistent then hardcoding because if I change 'detail' to 'info' then whole website detail view link breaks
        # return '/details/{slug}'.format(slug=self.slug)

    @property
    def name(self):
        return self.title

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
