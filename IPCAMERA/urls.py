from django.contrib import admin
from django.urls import path,include
from cameras import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cameras.urls')),
    
    ]