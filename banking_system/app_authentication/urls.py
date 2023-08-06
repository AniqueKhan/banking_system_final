from django.contrib.auth import views as AuthenticationViews
from django.urls import path
from app_authentication.views import *

urlpatterns = [
    path("login",login_view,name="login"),
    path("signup/",signup,name="signup"),
    path('logout/', AuthenticationViews.LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
]