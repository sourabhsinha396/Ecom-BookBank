from django.urls import path
from .views import login_page,signup,guest_register_view,RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',login_page,name="login"),
    path('signup/guest/',guest_register_view,name="guest_register"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('signup/',signup,name="signup"),
    path('class/signup/',RegisterView.as_view(),name="class-based-signup"),
]
