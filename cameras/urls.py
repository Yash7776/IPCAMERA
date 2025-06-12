from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('stream/', views.stream_camera, name='stream_camera'),
    path('add_camera/', views.add_camera, name='add_camera'),
    path('delete_camera/<str:camera_id>/', views.delete_camera, name='delete_camera'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)