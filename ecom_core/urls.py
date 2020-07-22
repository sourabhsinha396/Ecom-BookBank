from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('general_pages.urls')),
    path('',include('user_auth.urls')),
    path('',include('products.urls')),
    path('',include('carts.urls')),
    path('',include('orders.urls')),
    path('',include('billings.urls')),
    path('',include('marketting.urls')),
    path('api-auth/', include('rest_framework.urls')), #If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
