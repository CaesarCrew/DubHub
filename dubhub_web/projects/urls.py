from django.urls import path
from .views import *

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create-project'),
    path('list/', ProjectListView.as_view(), name='list-projects'),
    path('fotos/<str:arquivo>/', FotoProject.as_view(), name='foto-projects'),
]