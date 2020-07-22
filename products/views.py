# From Django Core
from django.http import Http404,JsonResponse
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.core import serializers

# From rest_framework
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

#From This folder
from .models import Product
from .serializers import ProductSerializer

#from custom app
from carts.models import Cart
from analytics.signals import object_viewed_signal
from analytics.mixins import ObjectViewedMixin

#--------------------------------Product LIST VIEW----------------------------------
def  product_list(request):
    '''Function Based View for Product List'''
    queryset = Product.objects.all()
    context  = {'object_list':queryset}
    return render(request,'products/product_list.html',context)


class ProductListView(ListView):
    '''Class Based View for Product List'''
    template_name = 'products/product_list.html' #default is appname/model_list.html
    queryset = Product.objects.all()


class ProductListAPI(generics.ListAPIView):
    ''' Api Based View powered by Django REST_FRAMEWORK'''
    # queryset = Product.objects.all() #Not needed since we are using get()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]   #Just 2 above lines are enough for browsable api
    template_name = 'products/product_list.html'

    def get(self, request):
        queryset = Product.objects.all()
        return Response({'object_list': queryset})

#------------------------------Product DETAIL_VIEW-------------------------------------
def product_detail(request,id):
    object  = get_object_or_404(Product,id=id)
    context = {'object':object}
    return render(request,'products/product_detail.html',context)


class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'


class ProductDetailAPI(ObjectViewedMixin,generics.RetrieveAPIView):
    # queryset = Product.objects.all() #Not needed since we are using get()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer] #Just 2 above lines are enough for browsable api
    template_name = 'products/product_detail.html'

    def get(self, request,pk):
        queryset = Product.objects.get(pk=pk)
        return Response({'object': queryset})

##--------------------------------------------------------------------###############
def get_million_copies_sold_book(request):
    qs = Product.objects.get_million_copies_book()
    context={'object_list':qs}
    return render(request,'products/million_copies_sold.html',context)



class GetMillionCopiesSoldBook(ListView):
    # queryset = Product.objects.all()
    template_name = 'products/million_copies_sold.html'

    def get_queryset(self,*args,**kwargs):
        ''' This functions helps to filter out and get actual queryset'''
        qs = Product.objects.get_million_copies_book()
        return qs

# For Rest-Framework it will be very similar to the ProductListAPI class with minor changes
class GetMillionCopiesSoldBookAPI(generics.ListAPIView):
    ''' Api Based View powered by Django REST_FRAMEWORK'''
    # queryset = Product.objects.all() #Not needed since we are using get()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]   #Just 2 above lines are enough for browsable api
    template_name = 'products/million_copies_sold.html'

    def get(self, request):
        queryset = Product.objects.get_million_copies_book()
        return Response({'object_list': queryset})


##----------------------------Product Detail by Slug ----------------------#######################
def product_details_by_slug(request,slug):
    '''This is the actual detail view that I am using'''
    try:
        object = get_object_or_404(Product,slug=slug)
    except Product.DoesNotExist:
        raise Http404("The Product You are searching for does not exists")
    except Product.MultipleObjectsReturned:
        queryset = Product.objects.filter(slug=slug,is_active=True)
        object = queryset.last()
    except:
        raise Http404("Ahhh I got a Headache Sorry!!!")

    object_viewed_signal.send(object.__class__,instance = object,request = request)
    context = {'object':object}
    return render(request,'products/product_detail.html',context)
##----------------------Auto Suggestions -----------------------------------####################
def autosuggest(request):
    print(request.GET)
    query_original = request.GET.get('term')
    queryset = Product.objects.filter(title__icontains=query_original)
    mylist= []
    mylist  += [x.title for x in queryset]
    return JsonResponse(mylist,safe=False)

##-----------------------Search Component in Navbar _________________________#######################
def products_search(request):
    ''' If I am intending to use this in other places also ,I should better put this in Model Manager'''
    query_original=request.GET.get('q',None)
    search_query = query_original.lower().split()
    if len(search_query)>=1:
        for word in search_query:
            lookups = Q(title__icontains=word) | Q(description__icontains=word) | Q(tags__name__icontains=word)
    queryset     = Product.objects.filter(lookups,is_active=True).distinct()
    #or Product.objects.active_only.filter()
    context      = {'object_list':queryset}
    return render(request,'products/product_search.html',context)
