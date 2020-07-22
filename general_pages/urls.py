from django.urls import path
from .views import home,contact,aboutus


urlpatterns = [
    path('',home,name="home"),
    path('aboutme/',aboutus,name="aboutme"),
    path('contactus/',contact,name="contact"),
]
