from django.urls import path
from .views import (product_list,ProductListView,
                    product_detail,ProductDetailView,
                    ProductListAPI,ProductDetailAPI,
                    get_million_copies_sold_book,GetMillionCopiesSoldBook,GetMillionCopiesSoldBookAPI,
                    product_details_by_slug,
                    products_search,
                    autosuggest
                    )

app_name = 'products' # This I added because if some other app is having the same url '/list/' then things will break
# with a namespace I call my URL as {% url 'products:detail' object.slug %}


urlpatterns = [
    #############--------Function Based------###############
    path('list/',product_list,name="func_product_list"),
    path('detail/<int:id>/',product_detail,name="func_product_detail"),
    path('details/<str:slug>/',product_details_by_slug,name="func_product_detail_by_slug"),
    path('bestseller/',get_million_copies_sold_book,name="million_copies"),
    path('product-search/',products_search,name="products_search"),
    path('autosuggest/',autosuggest,name="autosuggest"),




    ###############----Class Based--------################
    path('class/list/',ProductListView.as_view(),name="class_product_list"),
    path('class/detail/<int:pk>/',ProductDetailView.as_view(),name="class_product_detail"),
    path('class/million-copies/',GetMillionCopiesSoldBook.as_view(),name="class_million_copies"),



    ##############----Rest API -----##################
    path('api/list/',ProductListAPI.as_view(),name="api-list"),
    path('api/detail/<int:pk>/',ProductDetailAPI.as_view(),name="api-detail"),
    path('api/million-copies/',GetMillionCopiesSoldBookAPI.as_view(),name="api_million_copies"),
]
