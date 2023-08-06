from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("authentication/",include("app_authentication.urls")),
    path("",include("bank_management.urls")),
]
