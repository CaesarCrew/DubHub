from django.urls import path
from .views import FotoUser

urlpatterns = [
    path('fotos/<str:arquivo>/', FotoUser.as_view() , name='foto-user'),
]